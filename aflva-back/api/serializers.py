from rest_framework import serializers

from aeroflot.models import Flight, Book


class BookShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['status', 'altitude', 'speed', 'longitude', 'latitude']


class FlightSerializer(serializers.ModelSerializer):
    pilot = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Flight
        fields = ['fsuipc_data', 'pilot']
