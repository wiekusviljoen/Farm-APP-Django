from django.urls import path
from . import views
from . import views_admin

app_name = 'farm_app'

urlpatterns = [
    path('', views.farm_list, name='farm_list'),
    path('farm/create/', views.create_farm, name='create_farm'),
    path('api/feed-price/', views.feed_price_api, name='feed_price_api'),
    path('api/feed-prices/', views.feed_prices_list, name='feed_prices'),
    path('api/abattoir-prices/', views.abattoir_prices_list, name='abattoir_prices'),
    path('admin/trigger-abattoir-fetch/', views_admin.trigger_fetch_abattoirs, name='trigger_abattoir_fetch'),
    path('farm/<int:farm_id>/', views.farm_detail, name='farm_detail'),
    path('farm/<int:farm_id>/chatbot/', views.farm_chatbot, name='farm_chatbot'),
    path('farm/<int:farm_id>/chat/', views.send_chat_message, name='send_chat_message'),
    path('chatbot/', views.farm_chatbot, name='chatbot'),
    path('chat/', views.send_chat_message, name='send_chat_message_global'),
    path('cow/<int:cow_id>/', views.cow_detail, name='cow_detail'),
    path('bull/<int:bull_id>/', views.bull_detail, name='bull_detail'),
]
