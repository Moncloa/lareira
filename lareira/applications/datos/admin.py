from django.contrib import admin

# Register your models here.
from .models import Muestra, Sensor

admin.site.register(Muestra)
admin.site.register(Sensor)
