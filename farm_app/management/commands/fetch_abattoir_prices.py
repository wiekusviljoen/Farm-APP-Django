from django.core.management.base import BaseCommand
from django.utils import timezone
from farm_app.models import Abattoir
import urllib.request
import json

class Command(BaseCommand):
    help = 'Fetch live prices for all active abattoirs and update stored last_prices'

    def handle(self, *args, **options):
        count = 0
        for a in Abattoir.objects.filter(active=True):
            prices = {}
            if a.api_url:
                try:
                    req = urllib.request.Request(a.api_url)
                    with urllib.request.urlopen(req, timeout=8) as resp:
                        payload = json.load(resp)
                    for species, path in (a.species_json_paths or {}).items():
                        tmp = payload
                        for p in path.split('.') if path else []:
                            tmp = tmp.get(p) if isinstance(tmp, dict) else None
                        if isinstance(tmp, (int, float)) or (isinstance(tmp, str) and tmp.replace('.', '', 1).isdigit()):
                            prices[species] = float(tmp)
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'Fetch failed for {a.name}: {e}'))
            # Merge and update stored last_prices and last_fetched
            if prices:
                a.last_prices = {**(a.last_prices or {}), **prices}
                a.last_fetched = timezone.now()
                a.save()
                count += 1
                self.stdout.write(self.style.SUCCESS(f'Updated {a.name}: {prices}'))
            else:
                self.stdout.write(f'No new prices for {a.name}')

        self.stdout.write(self.style.SUCCESS(f'Done. Updated {count} abattoir(s).'))