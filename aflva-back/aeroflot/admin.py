from aeroflot.models import Pilot, Fleet, AircraftImage, Schedule, Book, Company, News, Flight
from django.contrib import admin
from django import forms
from django.urls import path
from django.db import models
from django.shortcuts import redirect


class AdminPilot(admin.ModelAdmin):
    model = Pilot
    list_display = ['callsign', 'name', 'email', 'status']
    list_editable = ['status']

    def email(self, obj):
        return obj.profile.email

    def name(self, obj):
        return f"{obj.profile.first_name} {obj.profile.last_name}"


admin.site.register(Pilot, AdminPilot)


class AircraftImageInline(admin.TabularInline):
    model = AircraftImage


class AdminCompany(admin.ModelAdmin):
    model = Company
    list_display = ('name', 'icao', 'iata', 'hub', 'logo')
    inlines = [AircraftImageInline]
    # def has_add_permission(self, request):
    #     return False
    # def has_change_permission(self, request, obj=None):
    #     return False
    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Company, AdminCompany)


class AdminFleet(admin.ModelAdmin):
    autocomplete_fields = ['now']
    model = Fleet
    list_filter = ("company", "aircraft_type")
    list_display = ('aircraft_registration', 'aircraft_type', 'now', 'status')


admin.site.register(Fleet, AdminFleet)
admin.site.register((News,))


class TimeForm(forms.ModelForm):
    deptime = forms.TimeField(widget=forms.TimeInput(format='%H:%M', attrs={'placeholder': '10:20'}))
    arrtime = forms.TimeField(widget=forms.TimeInput(format='%H:%M', attrs={'placeholder': '11:40'}))


class AdminSchedule(admin.ModelAdmin):
    model = Schedule
    form = TimeForm
    autocomplete_fields = ['dep_icao', 'arr_icao', 'alternate_icao']
    list_filter = ("company", "aircraft_type")
    list_display = ('flightnum', 'callsign', 'dep_icao', 'arr_icao', 'distance', 'deptime', 'arrtime')

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == 'aircraft_type':
            kwargs['widget'] = forms.CheckboxSelectMultiple()
            kwargs['help_text'] = ''
        return db_field.formfield(**kwargs)

    def get_form(self, request, obj=None, **kwargs):
        form = super(AdminSchedule, self).get_form(request, obj, **kwargs)
        fields = ["dep_icao", 'arr_icao', 'alternate_icao']
        for i in fields:
            field = form.base_fields[i]
            # field.widget.can_add_related = False
            field.widget.can_change_related = False
            field.widget.can_delete_related = False
        return form


admin.site.register(Schedule, AdminSchedule)


class RecalcModel(models.Model):
    class Meta:
        verbose_name_plural = '7. Recalculate All Flights and Hours'


def recalc_flights_hours():
    for i in Fleet.objects.all():
        i.flights = 0
        i.hours = 0
        i.save()
    for i in Pilot.objects.all():
        i.flights = 0
        i.hours = 0
        i.save()
    company = Company.objects.all()[0]
    company.flights = 0
    company.hours = 0
    company.save()
    flight = Flight.objects.all()
    for i in flight:
        pilot = Pilot.objects.get(id=i.pilot.id)
        fleet = Fleet.objects.get(aircraft_registration=i.aircraft_registration)
        company = Company.objects.all()[0]
        pilot.hours += i.flight_time
        pilot.flights += 1
        pilot.save()
        fleet.hours += i.flight_time
        fleet.flights += 1
        fleet.save()
        company.hours += i.flight_time
        company.flights += 1
        company.save()


def recalc_flights_hours_view(request):
    recalc_flights_hours()
    return redirect('admin:index')


class RecalcModelAdmin(admin.ModelAdmin):
    model = RecalcModel

    def get_urls(self):
        view_name = '{}_{}_changelist'.format(
            self.model._meta.app_label, self.model._meta.model_name)
        return [
            path('recalc_flights_hours/', recalc_flights_hours_view, name=view_name),
        ]


# admin.site.register(RecalcModel, RecalcModelAdmin)


class AdminBook(admin.ModelAdmin):
    model = Book
    list_display = [field.name for field in Book._meta.get_fields()]


admin.site.register(Book, AdminBook)


class AdminFlight(admin.ModelAdmin):
    model = Flight
    search_fields = ('pilot__callsign', 'flightnum')
    list_display = ('callsign', 'pilot')


admin.site.register(Flight, AdminFlight)

# class AdminStand(admin.ModelAdmin):
#     model = Stand
#     search_fields = ('airport__icao_code',)
#     autocomplete_fields = ['airport']
#
# admin.site.register(Stand,AdminStand)
