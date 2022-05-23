import json
import math
from datetime import datetime, timezone

import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from aeroflot.models import Flight
from .models import Penalty
from .serializers import *



def index(request):
    return render(request, 'index.html')


class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser,
    )

    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request):
        serializer = AuthCustomTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        content = {
            'token': token.key,
        }

        return Response(content)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def flight_upload(request):
    try:
        user_id = Token.objects.get(key=request.auth.key).user_id
        user = User.objects.get(id=user_id)
        if request.method == 'POST':
            res = json.loads(request.body)
            pilot = Pilot.objects.get(profile=user)
            flight = Flight()
            booking = Book.objects.get(id=res.get('booking'))
            fleet = Fleet.objects.get(id=booking.aircraft.id)
            if booking.schedule:
                flight.flightnum = booking.schedule.flightnum
            flight.company = booking.company
            flight.pilot = pilot
            flight.callsign = booking.callsign
            flight.aircraft_type = booking.aircraft.aircraft_type.aircraft_name
            flight.aircraft_registration = booking.aircraft.aircraft_registration
            flight.departure_airport = booking.dep_airport
            flight.arrival_airport = booking.arr_airport
            flight.flight_time = math.floor(res.get('flight_time'))
            flight.distance = res.get('distance_flown')
            flight.route = booking.route
            flight.pax = booking.pax
            flight.cargo = booking.cargo
            flight.fuel_used = res.get('dep_fuel') - res.get('landing_fuel')
            flight.fuel_left = res.get('landing_fuel')
            # vers = SimVersion.objects.all()
            # for i in res.get('processes'):
            #     if i in [j.app_exe for j in vers]:
            #         flight.sim_version = vers.get(app_exe = i)
            if res.get('zfw'):
                flight.zfw = res.get('zfw')
                flight.to_weight = res.get('to_weight')
                flight.landing_weight = res.get('landing_weight')
            flight.landing_vs = res.get('landing_vs')
            flight.dep_time = datetime.fromtimestamp(res.get('dep_time')).replace(tzinfo=timezone.utc)
            flight.arr_time = datetime.fromtimestamp(res.get('arr_time')).replace(tzinfo=timezone.utc)
            penalties = []
            if booking.arr_airport.icao_code in booking.company.hub.split(' '):
                penalties.append(Penalty.objects.filter(id=5))
            if res.get('stall'):
                penalties.append(Penalty.objects.filter(id=9))
            if res.get('moving'):
                penalties.append(Penalty.objects.filter(id=10))
            if res.get('crash'):
                penalties.append(Penalty.objects.filter(id=14))
            if res.get('landing_vs'):
                if -700 < res.get('landing_vs') < -500:
                    penalties.append(Penalty.objects.filter(id=8))
                elif -240 < res.get('landing_vs') < -80:
                    penalties.append(Penalty.objects.filter(id=4))
                elif -1600 < res.get('landing_vs') < -700:
                    penalties.append(Penalty.objects.filter(id=13))
                elif res.get('landing_vs') < -1600:
                    penalties.append(Penalty.objects.filter(id=14))
            if res.get('distance_flown'):
                if 1200 < res.get('distance_flown') < 1800:
                    penalties.append(Penalty.objects.filter(id=11))
                elif 1800 < res.get('distance_flown') < 3600:
                    penalties.append(Penalty.objects.filter(id=15))
                elif 3600 < res.get('distance_flown'):
                    penalties.append(Penalty.objects.filter(id=12))

            if res.get('overspeed'):
                penalties.append(Penalty.objects.filter(id=7))
            flight.save()
            for i in penalties:
                if i:
                    if i[0].rate > 0 or i[0].rate < 0:
                        flight.points += i[0].rate
                        flight.penalty.add(i[0].id)
            if flight.points < 1:
                flight.points = 1
            flight.save()
            booking.delete()
            return Response({'status': 'success'})
    except Exception as e:
        print(e)
        return Response({'error': str(e)})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def book_api(request):
    if request.method == 'GET':
        user_id = Token.objects.get(key=request.auth.key).user_id
        user = User.objects.get(id=user_id)
        pilot = Pilot.objects.get(profile=user)
        bookings = Book.objects.filter(pilot=pilot)
        serializer = BookSerializer(bookings, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book_status_api(request):
    try:
        req = request.POST
        user_id = Token.objects.get(key=request.auth.key).user_id
        user = User.objects.get(id=user_id)
        pilot = Pilot.objects.get(profile=user)
        bookings = Book.objects.filter(id=req.get('book_id'))
        if bookings:
            booking = bookings[0]
            booking.status = req.get('status')
            booking.altitude = req.get('altitude')
            booking.speed = req.get('speed')
            booking.longitude = req.get('longitude')
            booking.latitude = req.get('latitude')
            booking.save()
            return Response({'status': 'success'})
        else:
            return Response({'status': 'no booking found'})
    except Exception as e:
        return Response({'error': str(e)})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_api(request):
    user_id = Token.objects.get(key=request.auth.key).user_id
    user = User.objects.get(id=user_id)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def delete_booking_api(request):
    try:
        user_id = Token.objects.get(key=request.auth.key).user_id
        book = Book.objects.get(pilot=Pilot.objects.get(profile=user_id))
        book.delete()
        return Response({'status': 'success'})
    except Exception as e:
        return Response({'error': str(e)})


@api_view(['GET'])
def get_agent_api(request):
    try:
        agent = Agent.objects.all().order_by('id')[0]
        serializer = AgentSerializer(agent, many=False)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)})


def get_apt_data(request):
    icao = request.GET.get('icao')
    url = 'https://avwx.rest/api/station/' + icao
    header = {'Authorization': settings.AVWX_TOKEN}
    res = requests.get(url, headers=header)
    res = res.json()
    return JsonResponse(res)
