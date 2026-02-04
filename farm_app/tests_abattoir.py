from django.test import TestCase
from django.urls import reverse
from .models import Abattoir
from unittest.mock import patch
import io

class AbattoirTests(TestCase):
    def setUp(self):
        # Create abattoir with API URL and JSON paths
        self.a = Abattoir.objects.create(name='Test Abattoir', api_url='http://fake.local/api', species_json_paths={'cattle':'prices.cattle','sheep':'prices.sheep','goat':'prices.goat'})

    def fake_urlopen(self, req, timeout=5):
        class Ctx:
            def __enter__(self_non):
                return io.BytesIO(b'{"prices": {"cattle": 80.5, "sheep": 70.0, "goat": 65.25}}')
            def __exit__(self_non, exc_type, exc, tb):
                return False
        return Ctx()

    def test_abattoir_prices_api_returns_prices(self):
        with patch('urllib.request.urlopen', side_effect=self.fake_urlopen):
            url = reverse('farm_app:abattoir_prices')
            r = self.client.get(url)
            self.assertEqual(r.status_code, 200)
            data = r.json()
            self.assertIn('abattoirs', data)
            ab = data['abattoirs'][0]
            self.assertEqual(ab['name'], 'Test Abattoir')
            self.assertIn('prices', ab)
            self.assertEqual(float(ab['prices']['cattle']), 80.5)
            self.assertEqual(float(ab['prices']['sheep']), 70.0)
            self.assertEqual(float(ab['prices']['goat']), 65.25)

    def test_abattoir_prices_fallback_to_last_prices(self):
        # Populate last_prices and ensure returned when fetch fails
        from django.core.cache import cache
        cache.clear()
        self.a.last_prices = {'cattle': 90, 'sheep': 80}
        self.a.save()
        with patch('urllib.request.urlopen', side_effect=Exception('network')):
            url = reverse('farm_app:abattoir_prices')
            r = self.client.get(url)
            self.assertEqual(r.status_code, 200)
            data = r.json()
            ab = data['abattoirs'][0]
            self.assertEqual(float(ab['prices']['cattle']), 90.0)
            self.assertEqual(float(ab['prices']['sheep']), 80.0)
            self.assertIsNone(ab['prices'].get('goat'))
            # When fetch fails, API should include fetch_error
            self.assertIn('fetch_error', ab)
            self.assertIsNotNone(ab['fetch_error'])

    def test_trigger_fetch_endpoint_requires_staff(self):
        url = reverse('farm_app:trigger_abattoir_fetch')
        # Should redirect to login for anonymous
        r = self.client.get(url)
        self.assertEqual(r.status_code, 302)

    def test_trigger_fetch_endpoint_runs(self):
        from unittest.mock import patch
        with patch('farm_app.management.commands.fetch_abattoir_prices.Command.handle') as mock_handle:
            # Log in as staff
            from django.contrib.auth import get_user_model
            User = get_user_model()
            u = User.objects.create_user('staff', 's@e.com', 'pass')
            u.is_staff = True
            u.save()
            self.client.login(username='staff', password='pass')
            url = reverse('farm_app:trigger_abattoir_fetch')
            r = self.client.get(url)
            self.assertEqual(r.status_code, 200)
            data = r.json()
            self.assertIn('message', data)
            mock_handle.assert_called()