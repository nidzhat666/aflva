from rest_framework import serializers

from aeroflot.models import Flight, Book


class BookShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['status', 'altitude', 'speed', 'longitude', 'latitude']


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'
