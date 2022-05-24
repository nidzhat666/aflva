from django_countries.serializers import CountryFieldMixin
from django.contrib.auth import get_user_model
from rest_framework import serializers

from aeroflot.models import Flight, Book, Pilot, Company
from main.models import Profile
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
