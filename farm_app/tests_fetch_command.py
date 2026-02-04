from django.test import TestCase
from farm_app.management.commands.fetch_abattoir_prices import Command
from farm_app.models import Abattoir
from unittest.mock import patch
import io

class FetchCommandTests(TestCase):
    def setUp(self):
        self.a = Abattoir.objects.create(name='Cmd Abattoir', api_url='http://fake.local/api', species_json_paths={'cattle':'prices.cattle'})

    def fake_urlopen(self, req, timeout=5):
        class Ctx:
            def __enter__(self_non):
                return io.BytesIO(b'{"prices": {"cattle": 77.0}}')
            def __exit__(self_non, exc_type, exc, tb):
                return False
        return Ctx()

    def test_fetch_command_updates_abattoir(self):
        with patch('urllib.request.urlopen', side_effect=self.fake_urlopen):
            cmd = Command()
            cmd.handle()
            a = Abattoir.objects.get(pk=self.a.pk)
            self.assertIn('cattle', a.last_prices)
            self.assertEqual(float(a.last_prices['cattle']), 77.0)
            self.assertIsNotNone(a.last_fetched)
