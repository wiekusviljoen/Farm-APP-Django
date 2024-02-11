from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Farm, Cow, Bull

admin.site.register(Farm)
admin.site.register(Cow)
admin.site.register(Bull)
