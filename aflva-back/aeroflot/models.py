from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from main.models import Profile, AircraftType, AircraftICAO, Penalty, SimVersion
from airac.models import Airport
from main.scripts import dist_calculate
from django.contrib.auth.models import User
from django.db.models import Sum
from storages.backends.s3boto3 import S3Boto3Storage
import datetime, os


# Create your models here.

def get_file_path_company(instance, filename):
    ext = filename.split('.')[-1]
    return os.path.join(
        f'uploads/company/{instance.name}.{ext}')


class Company(models.Model):
    name = models.CharField(default='Aeroflot', max_length=10)
    callsign = models.CharField(max_length=100, blank=True, null=True)
    icao = models.CharField(default='AFL', max_length=10)
    iata = models.CharField(default='SU', max_length=10)
    hub = models.CharField(default='UUEE', max_length=10)
    logo = models.ImageField(storage=S3Boto3Storage(), upload_to=get_file_path_company)
    hours = models.IntegerField(editable=0, default=0)
    flights = models.IntegerField(editable=0, default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "1. Company"


class Pilot(models.Model):
    STATUS_CHOISE = (('Just Registred', 'Just Registred'), ('Inactive', 'Inactive'), ('Active', 'Active'))
    profile = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Pilot")
    callsign = models.CharField(default='AFL', max_length=10)
    status = models.CharField(max_length=100, choices=STATUS_CHOISE, default=STATUS_CHOISE[0][0], null=False,
                              blank=False)
    additional_flights = models.IntegerField(default=0)
    additional_hours = models.IntegerField(default=0,
                                           help_text='IN SECONDS!!! CONVERT HOURS TO SECONDS!!! For Example 2 hours = 7200 seconds')
    _flights_query, _flights, _hours, _rating = None, None, None, None

    @property
    def flights_query(self):
        if not self._flights_query:
            self._flights_query = self.flight.all()
        return self._flights_query

    @property
    def flights(self):
        if not self._flights:
            self._flights = self.flights_query.count()
            if not self._flights:
                self._flights = 0
        return self._flights

    @property
    def hours(self):
        if not self._hours:
            self._hours = sum([i.flight_time for i in self.flights_query])
            if not self._hours:
                self._hours = 0
        return self._hours

    @property
    def rating(self):
        if not self._rating:
            if self.flights:
                self._rating = int(sum([i.points for i in self.flights_query] + [100]) / (self.flights + 1))
            else:
                self._rating = 100
        return self._rating

    class Meta:
        verbose_name_plural = "2. Pilots"

    def __str__(self):
        return self.callsign


def get_file_path_fleet(instance, filename):
    ext = filename.split('.')[-1]
    return os.path.join(
        f'uploads/fleet/{instance.aircraft_registration}.{ext}')


class Fleet(models.Model):
    company = models.ForeignKey(Company, related_name='fleet', on_delete=models.PROTECT)
    STATUS_CHOISE = (('Inactive', 'Inactive'), ('Active', 'Active'), ('Stored', 'Stored'), ('Retro', 'Retro'))
    aircraft_type = models.ForeignKey(AircraftType, related_name='fleet', on_delete=models.CASCADE)
    aircraft_registration = models.CharField(max_length=10, verbose_name='Aircraft Registration', unique=True)
    aircraft_image = models.ImageField(storage=S3Boto3Storage(), upload_to=get_file_path_fleet)
    status = models.CharField(max_length=100, choices=STATUS_CHOISE, default=STATUS_CHOISE[0][0])
    now = models.ForeignKey(Airport, on_delete=models.PROTECT, related_name='fleet', null=True,
                            help_text='Example: UUEE')
    _flights_query, _flights, _hours, _rating = None, None, None, None

    @property
    def flights_query(self):
        if not self._flights_query:
            self._flights_query = Flight.objects.filter(aircraft_registration=self.aircraft_registration)
        return self._flights_query

    @property
    def flights(self):
        if not self._flights:
            self._flights = self.flights_query.count()
            if not self._flights:
                self._flights = 0
        return self._flights

    @property
    def hours(self):
        if not self._hours:
            self._hours = sum([i.flight_time for i in self.flights_query])
            if not self._hours:
                self._hours = 0
        return self._hours

    class Meta:
        verbose_name_plural = "3. Fleet"

    def __str__(self):
        return self.aircraft_registration


def get_file_path_ai(instance, filename):
    ext = filename.split('.')[-1]
    return os.path.join(
        f'uploads/ai/{instance.company.icao}_{instance.aircraft_icao}.{ext}')


class AircraftImage(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    aircraft_icao = models.ForeignKey(AircraftICAO, on_delete=models.CASCADE, related_name='aircraft_image')
    aircraft_image = models.ImageField(storage=S3Boto3Storage(), upload_to=get_file_path_ai)

    class Meta:
        verbose_name = 'Aircraft ICAO Image'
        verbose_name_plural = "4. Aircraft ICAO Image"
        unique_together = ('aircraft_icao', 'company',)

    def __str__(self):
        return self.aircraft_icao.aircraft_icao


class Schedule(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    STATUS_CHOISE = (('Inactive', 'Inactive'), ('Active', 'Active'))
    TYPE_CHOISE = (('Regular', 'Regular'), ('Fly-In', 'Fly-In'), ('Charter', 'Charter'))
    flightnum = models.CharField(max_length=100, help_text='Example: SU123', verbose_name='Flight Number', unique=True)
    callsign = models.CharField(max_length=100, help_text='Example: AFL123', verbose_name='Callsign')
    dep_icao = models.ForeignKey(Airport, on_delete=models.PROTECT, related_name='dep_icao', null=True,
                                 help_text='Example: UUEE', verbose_name='Departure Airport', )
    arr_icao = models.ForeignKey(Airport, on_delete=models.PROTECT, related_name='arr_icao', null=True,
                                 help_text='Example: UUEE', verbose_name='Arrival Airport')
    alternate_icao = models.ForeignKey(Airport, on_delete=models.PROTECT, related_name='alternate_icao', null=True,
                                       help_text='Example: UUEE', verbose_name='Alternative Airport')
    route = models.CharField(max_length=4000, help_text='Example: TOKNU L4 NUDKO T561 ODATI T875 GENPA',
                             verbose_name='Route')
    aircraft_type = models.ManyToManyField(AircraftICAO)
    flight_level = models.IntegerField(verbose_name='Flight Level', help_text='Example: 370')
    distance = models.IntegerField(verbose_name='Distance',
                                   help_text='Example: 350 in NM. It\'ll be calculated automatically if it\'ll be clear.',
                                   blank=True, null=True)
    deptime = models.TimeField(verbose_name='Departure Time', help_text='Example: 11:00', blank=True, null=True)
    arrtime = models.TimeField(verbose_name='Arrival Time', help_text='Example: 12:00', blank=True, null=True)
    flights = models.IntegerField(default=0, editable=False)
    hours = models.FloatField(default=0, editable=False)
    status = models.CharField(max_length=100, choices=STATUS_CHOISE, default=STATUS_CHOISE[0][0])
    flight_type = models.CharField(max_length=100, choices=TYPE_CHOISE, default=TYPE_CHOISE[0][0])
    payload_percentage = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True)

    class Meta:
        verbose_name_plural = "5. Schedule"

    def __str__(self):
        return self.flightnum + ' - ' + self.callsign

    def save(self, force_insert=False, force_update=False):
        if not self.distance:
            self.distance = round(
                dist_calculate(self.dep_icao.latitude, self.dep_icao.longitude, self.arr_icao.latitude,
                               self.arr_icao.longitude))
        super(Schedule, self).save(force_insert, force_update)


class Book(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, null=True, blank=True, related_name='book')
    schedule = models.ForeignKey(Schedule, on_delete=models.PROTECT, related_name='book', editable=False,
                                 blank=True, null=True)
    pilot = models.OneToOneField(Pilot, on_delete=models.PROTECT, related_name='book', editable=False)
    aircraft = models.OneToOneField(Fleet, related_name='book', on_delete=models.PROTECT, editable=False)
    callsign = models.CharField(max_length=100, unique=True, editable=False)
    dep_airport = models.ForeignKey(Airport, on_delete=models.PROTECT, related_name='dep_airport',
                                    help_text='Example: UUEE', verbose_name='Departure Airport', editable=False)
    arr_airport = models.ForeignKey(Airport, on_delete=models.PROTECT, related_name='arr_airport',
                                    help_text='Example: UUEE', verbose_name='Arrival Airport', editable=False)
    alternate_airport = models.ForeignKey(Airport, on_delete=models.PROTECT, null=True,
                                          related_name='alternate_icao_booking', help_text='Example: UUEE',
                                          verbose_name='Alternative Airport', editable=False)
    route = models.CharField(max_length=4000, help_text='Example: TOKNU L4 NUDKO T561 ODATI T875 GENPA',
                             verbose_name='Route')
    flight_level = models.IntegerField(verbose_name='Flight Level', help_text='Example: 370')
    distance = models.IntegerField(verbose_name='Distance',
                                   help_text='Example: 350 in NM. It\'ll be calculated automatically if it\'ll be clear.',
                                   blank=True, null=True)
    deptime = models.TimeField(verbose_name='Departure Time', help_text='Example: 11:00', blank=True, null=True)
    flight_time = models.TimeField()
    flight_type = models.CharField(max_length=100, blank=True, editable=False)
    pax = models.IntegerField(null=True)
    cargo = models.IntegerField(null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    altitude = models.IntegerField(null=True)
    speed = models.IntegerField(null=True)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __init__(self, *args, **kwargs):
        super(Book, self).__init__(*args, **kwargs)
        from django.utils.timezone import utc
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        if self.updated:
            timediff = now - self.updated
            if timediff.total_seconds() > 86400:
                self.delete()
        if self.status != "booked" and self.updated:
            timediff = now - self.updated
            if timediff.total_seconds() > 600:
                self.status = "booked"
                self.save()


class Flight(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, null=True, blank=True)
    pilot = models.ForeignKey(Pilot, on_delete=models.PROTECT, related_name='flight')
    flightnum = models.CharField(max_length=100, help_text='Example: SU123', verbose_name='Flight Number', blank=True,
                                 null=True)
    callsign = models.CharField(max_length=100, help_text='Example: AFL123', verbose_name='Callsign', null=True, blank=True)
    aircraft_type = models.CharField(max_length=100, verbose_name='Aircraft Type', null=True, blank=True)
    aircraft_registration = models.CharField(max_length=10, verbose_name='Aircraft Registration', null=True, blank=True)
    departure_airport = models.ForeignKey(Airport, on_delete=models.PROTECT, related_name='departure_airport',
                                          help_text='Example: UUEE', verbose_name='Departure Airport', null=True, blank=True)
    arrival_airport = models.ForeignKey(Airport, on_delete=models.PROTECT, related_name='arrival_airport',
                                        help_text='Example: UUEE', verbose_name='Arrival Airport', null=True, blank=True)
    dep_time = models.DateTimeField(verbose_name='Departure Time', help_text='Example: 11:00', blank=True, null=True)
    arr_time = models.DateTimeField(verbose_name='Arrival Time', help_text='Example: 11:00', blank=True, null=True)
    flight_time = models.IntegerField(blank=True, null=True)
    distance = models.IntegerField(blank=True, null=True)
    route = models.CharField(max_length=4000, help_text='Example: TOKNU L4 NUDKO T561 ODATI T875 GENPA',
                             verbose_name='Route')
    pax = models.IntegerField(null=True)
    cargo = models.IntegerField(null=True)
    landing_vs = models.IntegerField(blank=True, null=True)
    points = models.IntegerField(default=100, blank=True, null=True)
    penalty = models.ManyToManyField(Penalty, blank=True)
    fuel_used = models.IntegerField(default=0, blank=True, null=True)
    fuel_left = models.IntegerField(default=0, blank=True, null=True)
    zfw = models.IntegerField(default=0, blank=True, null=True)
    to_weight = models.IntegerField(default=0, blank=True, null=True)
    landing_weight = models.IntegerField(default=0, blank=True, null=True)
    sim_version = models.ForeignKey(SimVersion, on_delete=models.PROTECT, null=True, blank=True)
    fsuipc_data = models.JSONField(null=True)

    class Meta:
        verbose_name_plural = "7. Flight"

    # def save(self, *args, **kwargs):
    #     super(Flight, self).save(*args, **kwargs)
    #     fleet = Fleet.objects.get(aircraft_registration=self.aircraft_registration)
    #     profile = Profile.objects.get(user=self.pilot.profile)
    #     profile.now = self.arrival_airport.icao_code
    #     profile.save()
    #     fleet.now = self.arrival_airport
    #     fleet.save()


class News(models.Model):
    date = models.DateTimeField(auto_now=True, editable=False)
    text_ru = models.TextField()
    text_en = models.TextField()

    def __str__(self):
        return self.date.strftime("%d %B, %Y")

    class Meta:
        verbose_name_plural = "6. News"

# class Stand(models.Model):
#     company = models.ForeignKey(Company, on_delete=models.PROTECT)
#     airport = models.ForeignKey(Airport, on_delete=models.PROTECT)
#     stands = models.CharField(max_length=1000, help_text='Any stands/terminals information')
#
#     def __str__(self):
#         return self.airport.icao_code + " " + self.company.name
#     class Meta:
#         verbose_name_plural = "8. Stands"
