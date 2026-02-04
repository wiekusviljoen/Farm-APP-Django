from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Farm


class FarmCreateTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user('testuser', 't@e.com', 'pass')
        self.client = Client()

    def test_create_farm_assigns_owner_and_redirects(self):
        self.client.login(username='testuser', password='pass')
        url = reverse('farm_app:create_farm')
        data = {
            'name': 'New Farm',
            'location': 'Test Location',
            'cows_count': 5,
            'bulls_count': 1,
            'calf_count': 0,
            'feed_cost': 100,
        }
        response = self.client.post(url, data)
        # Should redirect to farm_detail
        self.assertEqual(response.status_code, 302)
        farm = Farm.objects.get(name='New Farm')
        self.assertEqual(farm.owner, self.user)

    def test_anonymous_redirects_to_login(self):
        url = reverse('farm_app:create_farm')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_feed_price_api_returns_price(self):
        url = reverse('farm_app:feed_price_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('price', data)
        self.assertIsInstance(data['price'], float)

    def test_feed_price_api_with_feed_and_quantity(self):
        # Simulate external API returning a specific price
        from unittest.mock import patch
        import io

        def fake_urlopen(req, timeout=5):
            class Ctx:
                def __enter__(self_non):
                    return io.BytesIO(b'{"price": 10.0}')
                def __exit__(self_non, exc_type, exc, tb):
                    return False
            return Ctx()

        with patch('urllib.request.urlopen', side_effect=fake_urlopen):
            with self.settings(FEED_PRICE_API_URL='http://fake.local'):
                url = reverse('farm_app:feed_price_api') + '?feed_type=Energie+Lek&quantity=3'
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                data = response.json()
                self.assertIn('price_per_unit', data)
                self.assertEqual(float(data['price_per_unit']), 10.0)
                self.assertIn('total', data)
                self.assertEqual(float(data['total']), 30.0)

    def test_feed_price_api_uses_api_key_header(self):
        # Ensure that when FEED_PRICE_API_KEY is set we send it as an Authorization header by default
        from unittest.mock import patch
        import io
        called = {}

        def fake_urlopen(req, timeout=5):
            # `req` should be a urllib.request.Request
            try:
                called['auth'] = req.get_header('Authorization')
            except Exception:
                called['auth'] = None
            class Ctx:
                def __enter__(self_non):
                    return io.BytesIO(b'{"price": 7.5}')
                def __exit__(self_non, exc_type, exc, tb):
                    return False
            return Ctx()

        with self.settings(FEED_PRICE_API_URL='http://fake.local', FEED_PRICE_API_KEY='mysecretkey'):
            with patch('urllib.request.urlopen', side_effect=fake_urlopen):
                url = reverse('farm_app:feed_price_api')
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                data = response.json()
                self.assertIn('price_per_unit', data)
                self.assertEqual(float(data['price_per_unit']), 7.5)
                # Default header uses 'Bearer ' prefix
                self.assertTrue(called.get('auth', '').startswith('Bearer '))

    def test_demo_mode_returns_varying_prices_when_no_provider(self):
        # When autodiscovery disabled and demo enabled, the endpoint should return randomized demo values
        from unittest.mock import patch
        with self.settings(FEED_PRICE_AUTODISCOVER=False, FEED_PRICE_DEMO=True):
            # Force deterministic randomness for test: two calls with different patched values
            with patch('random.random', side_effect=[0.1, 0.9]):
                url = reverse('farm_app:feed_price_api')
                r1 = self.client.get(url)
                r2 = self.client.get(url)
                self.assertEqual(r1.status_code, 200)
                self.assertEqual(r2.status_code, 200)
                d1 = r1.json()
                d2 = r2.json()
                self.assertIn('price_per_unit', d1)
                self.assertIn('price_per_unit', d2)
                self.assertNotEqual(d1['price_per_unit'], d2['price_per_unit'])

    def test_feed_prices_list_returns_prices(self):
        with self.settings(FEED_PRICE_AUTODISCOVER=False, FEED_PRICE_DEMO=True):
            url = reverse('farm_app:feed_prices')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn('prices', data)
            prices = data['prices']
            # Ensure we have the same number of entries as choices
            choices = list(__import__('farm_app.models', fromlist=['Farm']).Farm._meta.get_field('Feed').choices)
            self.assertEqual(len(prices), len(choices))
            for p in prices:
                self.assertIn('key', p)
                self.assertIn('label', p)
                self.assertIn('price', p)
                # 'None' feed choice should not have a price
                if p['key'] == 'None':
                    self.assertIsNone(p['price'])
                else:
                    self.assertIsInstance(p['price'], float)

    def test_none_feed_has_no_price_api(self):
        # When the explicit 'None' feed is requested, the API should return null prices
        url = reverse('farm_app:feed_price_api') + '?feed_type=None'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('price_per_unit', data)
        self.assertIsNone(data['price_per_unit'])
        # With quantity provided the total should also be null
        url = reverse('farm_app:feed_price_api') + '?feed_type=None&quantity=5'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsNone(data.get('total'))

    def test_provider_mapping_is_used_for_feed(self):
        # When a mapping exists, the mapped provider endpoint should be requested
        from unittest.mock import patch
        import io
        called = {}

        def fake_urlopen(req, timeout=5):
            # `req` may be a string or Request
            try:
                url = req.full_url
            except Exception:
                url = req
            called['url'] = str(url)
            class Ctx:
                def __enter__(self_non):
                    return io.BytesIO(b'{"price": 9.99}')
                def __exit__(self_non, exc_type, exc, tb):
                    return False
            return Ctx()

        mapping = {'Energie Lek': {'faostat_item': 'TESTCODE'}}
        with self.settings(FEED_PRICE_PROVIDER_MAP=mapping, FEED_PRICE_AUTODISCOVER=False):
            with patch('urllib.request.urlopen', side_effect=fake_urlopen):
                url = reverse('farm_app:feed_price_api') + '?feed_type=Energie+Lek'
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                data = response.json()
                self.assertIn('price_per_unit', data)
                self.assertEqual(float(data['price_per_unit']), 9.99)
                self.assertIn('TESTCODE', called.get('url', ''))

