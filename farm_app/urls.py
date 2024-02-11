from django.urls import path
from . import views

app_name = 'farm_app'

urlpatterns = [
    path('', views.farm_list, name='farm_list'),
    path('farm/<int:farm_id>/', views.farm_detail, name='farm_detail'),
    path('cow/<int:cow_id>/', views.cow_detail, name='cow_detail'),
    path('bull/<int:bull_id>/', views.bull_detail, name='bull_detail'),
]
