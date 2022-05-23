from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField
from django.contrib.auth import get_user_model

from .manager import UserManager


# class CustomUser(AbstractUser):
#     username = models.CharField(
#         _('username'),
#         max_length=150,
#         unique=False,
#         help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
#         error_messages={
#             'unique': _("A user with that username already exists."),
#         },
#         null=True,
#         blank=True
#     )
#     email = models.EmailField(_('email address'), unique=True)
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []
#     objects = UserManager()
#
#     def __str__(self):
#         return self.email + ' ' + self.get_full_name()


User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='profile')
    location = CountryField(verbose_name='Country', null=True, blank=True)
    flights = models.IntegerField(default=0, verbose_name='Flights', editable=False)
    hours = models.FloatField(default=0, verbose_name='Hours', editable=False)
    now = models.CharField(max_length=4, blank=True, null=True, help_text='Airport ICAO Code')
    ivaoid = models.IntegerField(verbose_name='Ivao ID', unique=True, blank=True, null=True)
    vatsimid = models.IntegerField(verbose_name='Vatsim ID', unique=True, blank=True, null=True)
    telegram_chat_id = models.IntegerField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name()


class AircraftICAO(models.Model):
    aircraft_icao = models.CharField(max_length=10, help_text="Example: A319", verbose_name='Aircraft ICAO Code',
                                     unique=True)
    flaps10 = models.IntegerField(help_text="Example: 230 in knots", verbose_name='Flaps 10° Speed')
    flaps15 = models.IntegerField(help_text="Example: 200 in knots", verbose_name='Flaps 15° Speed')
    flaps35 = models.IntegerField(help_text="Example: 177 in knots", verbose_name='Flaps 35° Speed')
    gear_up = models.IntegerField(help_text="Example: 260 in knots", verbose_name='Vmax Gear Up')
    gear_down = models.IntegerField(help_text="Example: 230 in knots", verbose_name='Vmax Gear Down')
    gear_cruise = models.IntegerField(help_text="Example: 300 in knots", verbose_name='Vmax Gear Cruise')
    max_pitch = models.FloatField(help_text="Example: 15 in °", verbose_name='Max Pitch')

    def __str__(self):
        return self.aircraft_icao

    class Meta:
        verbose_name = 'Aircraft Type'


class AircraftType(models.Model):
    EQUIPMENT_CHOISE = (
        ('/H', '/H'),
        ('/W', '/W'),
        ('/Z', '/Z'),
        ('/L', '/L'),
        ('/X', '/X'),
        ('/T', '/T'),
        ('/U', '/U'),
        ('/D', '/D'),
        ('/B', '/B'),
        ('/A', '/A'),
        ('/M', '/M'),
        ('/N', '/N'),
        ('/P', '/P'),
        ('/Y', '/Y'),
        ('/C', '/C'),
        ('/I', '/I'),
        ('/V', '/V'),
        ('/S', '/S'),
        ('/G', '/G'),
    )
    aircraft_icao = models.ForeignKey(AircraftICAO, related_name='aircraft_type', on_delete=models.CASCADE,
                                      verbose_name='Aircraft ICAO Code')
    aircraft_name = models.CharField(max_length=20, help_text="Example: Airbus A319-114", verbose_name='Aircraft Name',
                                     unique=True)
    aircraft_plan_suffix = models.CharField(max_length=20, help_text="Example: /L", choices=EQUIPMENT_CHOISE,
                                            verbose_name='Equipment Suffix')
    engine_type = models.CharField(max_length=20, help_text="Example: CFM56-5B5/P", verbose_name='Engine Type')
    flight_range = models.IntegerField(help_text="Example: 3700 in NM", verbose_name='Max Range')
    max_flightlevel = models.IntegerField(help_text="Example: 380 in FL", verbose_name='Max Flight Level')
    cruise_speed = models.IntegerField(help_text="Example: 455 in knots", verbose_name='Cruise Speed')
    empty_weight = models.IntegerField(help_text="Example: 41513 in KGS", verbose_name='Empty Weight')
    max_weight = models.IntegerField(help_text="Example: 70400 in KGS", verbose_name='Max Weight')
    landing_weight = models.IntegerField(help_text="Example: 61000 in KGS", verbose_name='Landing Weight')
    fuel = models.IntegerField(help_text="Example: 61000 in KGS", verbose_name='Fuel Load')
    payload = models.IntegerField(help_text="Example: 15500 in KGS", verbose_name='Payload')
    pax = models.IntegerField(help_text="Example: 150", verbose_name='Pax')

    class Meta:
        verbose_name = 'Aircraft Type'

    def __str__(self):
        return self.aircraft_name


class Agent(models.Model):
    agent_version = models.CharField(max_length=20, help_text="Example: 1.0.1",
                                     verbose_name="DEVELOPER ONLY! Agent Version")
    agent_file = models.FileField(verbose_name="DEVELOPER ONLY! Agent File")

    class Meta:
        verbose_name = 'DEVELOPER ONLY! Agent'


class Penalty(models.Model):
    name = models.CharField(max_length=100, help_text='Example: Perfect Landing', verbose_name='Penalty Name En',
                            null=True, blank=True)
    name_ru = models.CharField(max_length=100, help_text='Example: Отличная Посадка', verbose_name='Penalty Name Rus',
                               null=True, blank=True)
    rate = models.IntegerField(help_text='Example: 10 or -10 ...', verbose_name='Rate', )


class SimVersion(models.Model):
    app_exe = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name
