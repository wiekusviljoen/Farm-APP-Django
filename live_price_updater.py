import os
import django
import threading
import time
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farm_project.settings')
django.setup()

from django.core.management import call_command
from django.utils import timezone
from django.core.cache import cache
from farm_app.models import Abattoir
import random

class PriceUpdater:
    """Background task to update abattoir prices with staggered updates for realistic ticker effect"""
    
    def __init__(self, update_interval=0.2):  # 200ms for staggered updates
        self.update_interval = update_interval
        self.running = True
        self.thread = None
        self.last_update_time = {}  # Track when each abattoir was last updated
    
    def update_single_price(self, abattoir):
        """Update a single abattoir's prices with dramatic fluctuations (±N$1) for demo visibility"""
        try:
            # Save current prices as previous (for price change tracking)
            if abattoir.last_prices:
                cache.set(f'abattoir_prev_prices_{abattoir.id}', abattoir.last_prices, 3600)
            else:
                # Initialize if not set
                abattoir.last_prices = {'cattle': 45.5, 'sheep': 32.0, 'goat': 38.75}
                cache.set(f'abattoir_prev_prices_{abattoir.id}', abattoir.last_prices, 3600)
            
            # Apply dramatic fluctuation (±N$1) for each species
            prices = {}
            for species in ['cattle', 'sheep', 'goat']:
                current = abattoir.last_prices.get(species, 45.5 if species == 'cattle' else (32.0 if species == 'sheep' else 38.75))
                # Random change between -1 and +1 per update
                change = random.uniform(-1.0, 1.0)
                new_price = max(current + change, 10.0)  # Minimum price floor
                prices[species] = round(new_price, 2)
            
            # Update the abattoir
            abattoir.last_prices = prices
            abattoir.last_fetched = timezone.now()
            abattoir.save()
        
        except Exception as e:
            print(f'Error updating prices: {e}')
    
    def run(self):
        """Run the price updater in a loop, updating each abattoir separately"""
        print(f'[{datetime.now().strftime("%H:%M:%S")}] Starting price updater (staggered updates every {self.update_interval}s)...')
        
        abattoirs = list(Abattoir.objects.filter(active=True))
        update_index = 0
        
        while self.running:
            try:
                # Cycle through each abattoir, updating one at a time
                if abattoirs:
                    a = abattoirs[update_index % len(abattoirs)]
                    self.update_single_price(a)
                    update_index += 1
                
                time.sleep(self.update_interval)
            except KeyboardInterrupt:
                print('Stopping price updater...')
                self.running = False
                break
            except Exception as e:
                print(f'Unexpected error: {e}')
                time.sleep(self.update_interval)
    
    def start(self):
        """Start the price updater in a background thread"""
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Stop the price updater"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)

if __name__ == '__main__':
    # Create and start the price updater
    updater = PriceUpdater(update_interval=0.2)  # Update 200ms apart for staggered effect
    updater.start()
    
    print('\n' + '='*60)
    print('Live Abattoir Price Updater Running')
    print('='*60)
    print('Prices will update separately with staggered timing')
    print('Each abattoir updates in sequence for realistic ticker effect')
    print('Press CTRL+C to stop\n')
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('\nStopping updater...')
        updater.stop()
        print('Updater stopped.')
