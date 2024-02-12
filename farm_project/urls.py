from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("user_auth.urls")),
    path('farm_app/', include('farm_app.urls')),  # Include your app's URLs
    path('user_auth/', include("django.contrib.auth.urls")), 
    
    
    
]
