from django.shortcuts import render, get_object_or_404, redirect
from .models import Farm, Cow, Bull, Abattoir
from .forms import FarmForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from django.core.cache import cache
from django.utils import timezone
import json
import urllib.request
from django.conf import settings


@login_required
def farm_list(request):
    # Show only farms that belong to the logged-in user
    farms = Farm.objects.filter(owner=request.user)

    # Calculate totals based on user's farms (use aggregate sums to avoid unrelated global counts)
    total_cows = sum(f.cows_count for f in farms)
    total_bulls = sum(f.bulls_count for f in farms)
    total_cattle = total_cows + total_bulls
    return render(request, 'farm_app/farm_list.html', {'farm_list': farms, 'total_cattle': total_cattle})


@login_required
def farm_detail(request, farm_id):
    # Ensure users can only access their own farms
    farm = get_object_or_404(Farm, pk=farm_id, owner=request.user)
    return render(request, 'farm_app/farm_detail.html', {'farm': farm})


@login_required
def create_farm(request):
    if request.method == 'POST':
        form = FarmForm(request.POST)
        if form.is_valid():
            farm = form.save(commit=False)
            farm.owner = request.user
            farm.save()
            messages.success(request, 'Farm created successfully.')
            return redirect('farm_app:farm_detail', farm_id=farm.id)
    else:
        form = FarmForm()
    return render(request, 'farm_app/farm_form.html', {'form': form})


def _get_price_for_feed(feed_type=None):
    """Internal helper: returns a float price or None.

    Special case: when feed_type is explicitly 'None' (the choice value), treat as having no price
    and do not perform autodiscovery or demo fallback.
    """
    if feed_type and isinstance(feed_type, str) and feed_type.strip().lower() == 'none':
        return None

    api_url = getattr(settings, 'FEED_PRICE_API_URL', None)
    json_path = getattr(settings, 'FEED_PRICE_JSON_PATH', 'price')
    api_key = getattr(settings, 'FEED_PRICE_API_KEY', None)
    header_name = getattr(settings, 'FEED_PRICE_API_KEY_HEADER_NAME', 'Authorization')
    key_prefix = getattr(settings, 'FEED_PRICE_API_KEY_PREFIX', 'Bearer ')
    query_param = getattr(settings, 'FEED_PRICE_API_KEY_QUERY_PARAM', None)
    autodiscover = getattr(settings, 'FEED_PRICE_AUTODISCOVER', True)
    demo_mode = getattr(settings, 'FEED_PRICE_DEMO', True)

    price = None
    # 1) If there is a provider mapping for this feed, try the mapped provider first
    provider_map = getattr(settings, 'FEED_PRICE_PROVIDER_MAP', {}) or {}
    if feed_type and provider_map.get(feed_type):
        map_entry = provider_map.get(feed_type)
        # currently support faostat_item mapping
        fao_item = map_entry.get('faostat_item')
        if fao_item:
            try:
                fao_url = f'https://fenixservices.fao.org/faostat/api/v1/en/Prices?item={urllib.parse.quote(fao_item)}'
                with urllib.request.urlopen(fao_url, timeout=6) as resp:
                    data = json.load(resp)
                # attempt to read 'price' or common keys
                if isinstance(data, dict):
                    for k in ('price', 'value', 'usd'):
                        v = data.get(k)
                        if isinstance(v, (int, float)) or (isinstance(v, str) and v.replace('.', '', 1).isdigit()):
                            price = float(v)
                            break
            except Exception as e:
                print('mapped provider fetch failed:', e)
                price = None

    # 2) Try configured provider
    if price is None and api_url:
        try:
            url = api_url
            params = {}
            if feed_type:
                params['feed_type'] = feed_type
            if query_param and api_key:
                params[query_param] = api_key
            if params:
                sep = '&' if '?' in url else '?'
                url = url + sep + urllib.parse.urlencode(params)

            req = urllib.request.Request(url)
            if api_key and (not query_param):
                req.add_header(header_name, key_prefix + api_key)

            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.load(resp)

            parts = json_path.split('.') if json_path else ['price']
            tmp = data
            for p in parts:
                tmp = tmp.get(p) if isinstance(tmp, dict) else None
            price = tmp
        except Exception as e:
            print('feed provider fetch failed:', e)
            price = None
    # Autodiscover public endpoints
    if price is None and autodiscover and feed_type:
        candidates = [
            'https://fenixservices.fao.org/faostat/api/v1/en/Prices?item={feed_type}',
            'https://api.worldbank.org/v2/commodities/{feed_type}?format=json',
        ]
        for cand in candidates:
            try:
                url = cand.format(feed_type=urllib.parse.quote(feed_type))
            except Exception:
                url = cand
            try:
                with urllib.request.urlopen(url, timeout=6) as resp:
                    data = json.load(resp)
                if isinstance(data, dict):
                    for k in ('price', 'value', 'usd'):
                        v = data.get(k)
                        if isinstance(v, (int, float)) or (isinstance(v, str) and v.replace('.', '', 1).isdigit()):
                            price = float(v)
                            break
                elif isinstance(data, list) and len(data) > 0:
                    first = data[0]
                    if isinstance(first, dict):
                        for k in ('price', 'value', 'usd'):
                            v = first.get(k)
                            if isinstance(v, (int, float)) or (isinstance(v, str) and v.replace('.', '', 1).isdigit()):
                                price = float(v)
                                break
                if price is not None:
                    break
            except Exception as e:
                print('autodiscover candidate failed:', e)
                continue

    # Demo fallback
    if price is None:
        if demo_mode:
            import random
            base = 80.0
            price = round(base + random.random() * 40.0, 2)
        else:
            price = None

    try:
        return float(price)
    except Exception:
        return None


@login_required
@require_GET
def feed_price_api(request):
    """Return a JSON object with the latest feed price and optional computed totals.

    Behavior:
    - Accepts optional GET params: `feed_type` and `quantity` (float). If `quantity` is provided the
      response will include `total` = price_per_unit * quantity.
    """
    feed_type = request.GET.get('feed_type')
    quantity = request.GET.get('quantity')
    quantity_val = None
    try:
        if quantity is not None:
            quantity_val = float(quantity)
    except Exception:
        quantity_val = None

    price = _get_price_for_feed(feed_type)
    result = {}
    if price is None:
        if feed_type:
            # An explicit feed was requested but has no price (e.g., the "None" choice)
            result['price_per_unit'] = None
            result['price'] = None
            if quantity_val is not None:
                result['total'] = None
        else:
            # No feed specified -- preserve legacy default behavior
            price = 120.00
            result['price_per_unit'] = round(price, 2)
            result['price'] = round(price, 2)
            if quantity_val is not None:
                result['total'] = round(price * quantity_val, 2)
    else:
        result['price_per_unit'] = round(price, 2)
        result['price'] = round(price, 2)
        if quantity_val is not None:
            result['total'] = round(price * quantity_val, 2)
    return JsonResponse(result)


@login_required
@require_GET
def feed_prices_list(request):
    """Return prices for all known feed types as JSON list: [{'key','label','price'}]"""
    # Get choices from the Farm model field
    choices = list(Farm._meta.get_field('Feed').choices)
    out = []
    for key, label in choices:
        price = _get_price_for_feed(key)
        out.append({'key': key, 'label': label, 'price': round(price, 2) if price is not None else None})
    return JsonResponse({'prices': out})


@require_GET
def abattoir_prices_list(request):
    """Return list of active abattoirs with live prices per species (N$ per kg).

    Response format: { 'abattoirs': [ { 'id','name','location','prices': {'cattle': 80.0, 'sheep': 90.0, 'goat': 85.0}, 'last_fetched': timestamp_or_null }, ... ] }
    """
    # Don't cache - always fetch fresh data for live updates
    cache_key = 'abattoir_prices'

    out = []
    # Fetch active abattoirs directly from database
    abattoirs = list(Abattoir.objects.filter(active=True))
    stale_threshold = getattr(settings, 'ABATTOIR_PRICE_STALE_THRESHOLD_MINUTES', 10)
    
    for a in abattoirs:
        prices = {}
        price_changes = {}
        fetch_error = None
        
        # Use stored last_prices (which are updated by management commands)
        if a.last_prices:
            prices = a.last_prices
            
            # Get previous prices for change calculation
            prev_prices = cache.get(f'abattoir_prev_prices_{a.id}')
            if prev_prices:
                # Calculate percentage changes
                for species in prices:
                    current = prices[species]
                    previous = prev_prices.get(species, current)
                    if previous > 0:
                        change_percent = ((current - previous) / previous) * 100
                        change = current - previous
                        price_changes[species] = {
                            'change': round(change, 2),
                            'change_percent': round(change_percent, 2),
                            'direction': 'up' if change > 0 else ('down' if change < 0 else 'flat')
                        }
        
        # Determine staleness (if prices haven't been updated in 10+ minutes)
        stale = False
        if a.last_fetched:
            delta = timezone.now() - a.last_fetched
            stale = delta.total_seconds() > (stale_threshold * 60)

        out.append({
            'id': a.id,
            'name': a.name,
            'location': a.location,
            'prices': prices or None,
            'price_changes': price_changes or None,
            'last_fetched': (a.last_fetched.isoformat() if a.last_fetched else None),
            'fetch_error': fetch_error,
            'stale': stale,
        })

    return JsonResponse({'abattoirs': out})

@login_required
def cow_detail(request, cow_id):
    # Get the cow and ensure it belongs to one of the user's farms
    cow = get_object_or_404(Cow, pk=cow_id)
    # If needed, add farm association verification here
    return render(request, 'farm_app/cow_detail.html', {'cow': cow})

@login_required
def bull_detail(request, bull_id):
    # Get the bull and ensure it belongs to one of the user's farms
    bull = get_object_or_404(Bull, pk=bull_id)
    # If needed, add farm association verification here
    return render(request, 'farm_app/bull_detail.html', {'bull': bull})
