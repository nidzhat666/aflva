from django.contrib import admin
from .models import Airport
from django import forms
# Register your models here.



class AdminAirport(admin.ModelAdmin):
    change_form_template = 'admin/airac/custom_change_form.html'
    model = Airport
    search_fields = ['icao_code']
    list_display = ('icao_code','iata_code','city','country','elevation','latitude','longitude')

admin.site.register(Airport,AdminAirport)