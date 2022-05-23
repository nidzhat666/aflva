from django_countries.serializers import CountryFieldMixin
from django.contrib.auth import get_user_model
from rest_framework import serializers

from aeroflot.models import Flight, Book, Pilot
from main.models import Profile

User = get_user_model()


class BookShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['status', 'altitude', 'speed', 'longitude', 'latitude']


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'


class PilotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pilot
        fields = '__all__'


class ProfileSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'flights', 'hours', 'ivaoid', 'location', 'now', 'vatsimid')


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)
    pilot = PilotSerializer(many=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'get_full_name', 'email', 'profile', 'pilot']
