from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

from aeroflot.models import Book, Pilot, Fleet, Company
from airac.models import Airport
from .models import Agent, AircraftICAO, AircraftType

User = get_user_model()


class AuthCustomTokenSerializer(serializers.Serializer):
    email_or_username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email_or_username = attrs.get('email_or_username')
        password = attrs.get('password')

        if email_or_username and password:
            # Check if user sent email
            if User.objects.filter(email=email_or_username):
                user_request = User.objects.get(email=email_or_username)
                email_or_username = user_request.username
                user = authenticate(username=email_or_username, password=password)

            elif User.objects.filter(username=email_or_username):
                user_request = User.objects.get(username=email_or_username)
                email_or_username = user_request.username
                user = authenticate(username=email_or_username, password=password)
            else:
                error = {'message': "Unknown Error"}
                raise serializers.ValidationError(error)
        attrs['user'] = user
        return attrs


class AircraftICAOSerializer(serializers.ModelSerializer):
    class Meta:
        model = AircraftICAO
        fields = '__all__'


class AircraftTypeSerializer(serializers.ModelSerializer):
    aircraft_icao = AircraftICAOSerializer(read_only=True)

    class Meta:
        model = AircraftType
        fields = '__all__'


class FleetSerializer(serializers.ModelSerializer):
    aircraft_type = AircraftTypeSerializer(read_only=True)

    class Meta:
        model = Fleet
        fields = '__all__'


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ('agent_version',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'get_full_name', 'email']


class PilotSerializer(serializers.ModelSerializer):
    permission_classes = (IsAuthenticated,)
    profile = UserSerializer(read_only=True)

    class Meta:
        model = Pilot
        fields = '__all__'


class AirportSerializer(serializers.ModelSerializer):
    permission_classes = (IsAuthenticated,)

    class Meta:
        model = Airport
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    permission_classes = (IsAuthenticated,)

    class Meta:
        model = Company
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    permission_classes = (IsAuthenticated,)
    dep_airport = AirportSerializer(read_only=True)
    arr_airport = AirportSerializer(read_only=True)
    alternate_airport = AirportSerializer(read_only=True)
    pilot = PilotSerializer(read_only=True)
    aircraft = FleetSerializer(read_only=True)
    company = CompanySerializer(read_only=True)

    class Meta:
        model = Book
        fields = '__all__'
