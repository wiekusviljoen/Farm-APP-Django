from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from farm_app.management.commands.fetch_abattoir_prices import Command

@staff_member_required
def trigger_fetch_abattoirs(request):
    """Endpoint to trigger an immediate fetch of all active abattoirs (admin-only).

    Returns JSON: { 'updated': <n>, 'message': '...' }
    """
    cmd = Command()
    # We reuse the management command logic; capture stdout by calling handle and returning success message.
    cmd.handle()
    return JsonResponse({'updated': 'see logs', 'message': 'Fetch started (check admin messages and logs)'} )