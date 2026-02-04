import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farm_project.settings')
django.setup()

from farm_app.models import Abattoir

# Create sample abattoirs
abattoirs_data = [
    {
        'name': 'Windhoek Central',
        'location': 'Windhoek',
        'api_url': None,
        'species_json_paths': {'cattle': 'price', 'sheep': 'price', 'goat': 'price'},
        'last_prices': {'cattle': 45.50, 'sheep': 32.00, 'goat': 38.75},
        'active': True
    },
    {
        'name': 'Otjiwarongo Abattoir',
        'location': 'Otjiwarongo',
        'api_url': None,
        'species_json_paths': {'cattle': 'price', 'sheep': 'price', 'goat': 'price'},
        'last_prices': {'cattle': 44.00, 'sheep': 31.50, 'goat': 37.50},
        'active': True
    },
    {
        'name': 'Walvis Bay Processor',
        'location': 'Walvis Bay',
        'api_url': None,
        'species_json_paths': {'cattle': 'price', 'sheep': 'price', 'goat': 'price'},
        'last_prices': {'cattle': 46.75, 'sheep': 33.25, 'goat': 40.00},
        'active': True
    }
]

for data in abattoirs_data:
    obj, created = Abattoir.objects.get_or_create(
        name=data['name'],
        defaults=data
    )
    if created:
        print(f'Created: {obj.name}')
    else:
        print(f'Already exists: {obj.name}')

print(f'Total abattoirs: {Abattoir.objects.count()}')
