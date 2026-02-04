from django.contrib import admin
from .models import Farm, Cow, Bull, Abattoir


@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'owner', 'cows_count', 'bulls_count')
    list_filter = ('owner',)
    search_fields = ('name', 'location', 'owner__username')


@admin.register(Cow)
class CowAdmin(admin.ModelAdmin):
    list_display = ('name', 'breed', 'age', 'weight')


@admin.register(Bull)
class BullAdmin(admin.ModelAdmin):
    list_display = ('name', 'breed', 'age', 'weight')


@admin.register(Abattoir)
class AbattoirAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'api_url', 'active', 'last_fetched')
    list_filter = ('active',)
    search_fields = ('name', 'location')
    readonly_fields = ('last_fetched', 'last_prices')
    actions = ('fetch_now_action',)
    fieldsets = (
        (None, {'fields': ('name', 'location', 'api_url', 'species_json_paths', 'active')}),
        ('Last fetched', {'fields': ('last_fetched', 'last_prices')}),
    )

    def fetch_now_action(self, request, queryset):
        """Admin action to fetch prices for selected abattoirs immediately."""
        from django.utils import timezone
        import urllib.request, json
        updated = 0
        for a in queryset:
            prices = {}
            try:
                if a.api_url:
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
                self.message_user(request, f'Fetch failed for {a.name}: {e}', level='warning')
            if prices:
                a.last_prices = {**(a.last_prices or {}), **prices}
                a.last_fetched = timezone.now()
                a.save()
                updated += 1
        self.message_user(request, f'Updated {updated} abattoir(s).')
    fetch_now_action.short_description = 'Fetch prices now for selected abattoirs'
