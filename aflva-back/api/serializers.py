from django_countries.serializers import CountryFieldMixin
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import serializers

from aeroflot.models import Flight, Book, Pilot, Company, Schedule, Fleet, AircraftImage
from main.models import Profile, AircraftICAO, AircraftType
from main.serializers import AirportSerializer, FleetSerializer

User = get_user_model()


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'


class PilotSerializer(serializers.ModelSerializer):
    now = AirportSerializer()

    class Meta:
        model = Pilot
        fields = ('id', 'callsign', 'status', 'hours', 'flights', 'rating', 'now')


class ProfileSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'ivaoid', 'location', 'vatsimid')


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    pilot = PilotSerializer()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'get_full_name', 'email', 'profile', 'pilot']


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name', 'callsign', 'icao', 'iata', 'hub', 'logo')


class CompanyDedicatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name', 'callsign', 'icao', 'iata', 'hub', 'logo', 'is_retro')


class UserPublicSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'get_full_name', 'profile']


class Pilot4BookSerializer(serializers.ModelSerializer):
    now = AirportSerializer()
    profile = UserSerializer()

    class Meta:
        model = Pilot
        fields = ('id', 'callsign', 'status', 'hours', 'flights', 'rating', 'now', 'profile')


class BookShortSerializer(serializers.ModelSerializer):
    pilot = Pilot4BookSerializer()
    company = CompanySerializer()
    aircraft = FleetSerializer()
    dep_airport = AirportSerializer()
    arr_airport = AirportSerializer()

    class Meta:
        model = Book
        fields = ['status', 'altitude', 'speed', 'longitude', 'latitude', 'pilot', 'company', 'callsign', 'aircraft', 'dep_airport', 'arr_airport']


class PilotTopSerializer(serializers.ModelSerializer):
    flight_count = serializers.IntegerField()
    average_rating = serializers.IntegerField()

    class Meta:
        model = Pilot
        fields = ('full_name', 'flight_count', 'average_rating')


class ScheduleSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    dep_icao = AirportSerializer()
    arr_icao = AirportSerializer()
    alternate_icao = AirportSerializer()
    flight_time = serializers.DateTimeField(format='%H:%M')
    deptime = serializers.TimeField(format='%H:%M')
    arrtime = serializers.TimeField(format='%H:%M')
    avail = serializers.BooleanField()
    booked = serializers.BooleanField()

    class Meta:
        model = Schedule
        fields = ('company', 'flightnum', 'callsign', 'dep_icao', 'arr_icao', 'alternate_icao',
                  'route', 'flight_level', 'distance', 'deptime', 'arrtime', 'payload_percentage',
                  'flight_time', 'avail', 'booked')


class AircraftImageSerializer(serializers.ModelSerializer):
    aircraft_icao = serializers.SlugRelatedField(slug_field='aircraft_icao', read_only=True)

    class Meta:
        model = AircraftImage
        fields = '__all__'


class AircraftTypeV2Serializer(serializers.ModelSerializer):
    class Meta:
        model = AircraftType
        fields = '__all__'


class FleetV2Serializer(serializers.ModelSerializer):
    aircraft_type = AircraftTypeV2Serializer()
    icao = serializers.CharField()
    icao_image = serializers.SerializerMethodField()
    now = AirportSerializer()
    avail = serializers.BooleanField()
    booked = serializers.BooleanField(source='book')

    class Meta:
        model = Fleet
        fields = ('id', 'company', 'aircraft_type', 'aircraft_registration', 'aircraft_image',
                  'status', 'now', 'icao', 'icao_image', 'avail', 'booked')

    def get_icao_image(self, obj):
        return f'{settings.AWS_S3_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/{obj.icao_image}'
