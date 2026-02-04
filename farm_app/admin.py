from django.contrib import admin
from .models import Farm, Cow, Bull, Abattoir, ChatMessage


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

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'farm', 'created_at', 'message_preview')
    list_filter = ('created_at', 'farm', 'user')
    search_fields = ('user__username', 'farm__name', 'user_message')
    readonly_fields = ('created_at', 'user_message', 'ai_response', 'user')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Conversation Info', {'fields': ('user', 'farm', 'created_at')}),
        ('User Message', {'fields': ('user_message',)}),
        ('AI Response', {'fields': ('ai_response',)}),
    )
    
    def message_preview(self, obj):
        """Show preview of user message."""
        preview = obj.user_message[:50]
        if len(obj.user_message) > 50:
            preview += '...'
        return preview
    message_preview.short_description = 'Message'
    
    def has_add_permission(self, request):
        """Prevent manual addition through admin."""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Allow deletion through admin."""
        return True