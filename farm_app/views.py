from django.shortcuts import render, get_object_or_404
from .models import Farm, Cow, Bull

from django.shortcuts import render
from .models import Farm, Cow, Bull

def farm_list(request):
    farms = Farm.objects.all()
    total_cows = Cow.objects.count()
    total_bulls = Bull.objects.count()
    total_cattle = total_cows + total_bulls
    return render(request, 'farm_app/farm_list.html', {'farm_list': farms, 'total_cattle': total_cattle})


def farm_detail(request, farm_id):
    farm = get_object_or_404(Farm, pk=farm_id)
    return render(request, 'farm_app/farm_detail.html', {'farm': farm})

def cow_detail(request, cow_id):
    cow = get_object_or_404(Cow, pk=cow_id)
    return render(request, 'farm_app/cow_detail.html', {'cow': cow})

def bull_detail(request, bull_id):
    bull = get_object_or_404(Bull, pk=bull_id)
    return render(request, 'farm_app/bull_detail.html', {'bull': bull})

