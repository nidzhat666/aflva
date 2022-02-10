from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from aeroflot.models import Book
from main.models import Penalty
from .serializers import FlightSerializer, BookShortSerializer


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookShortSerializer
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all().select_related('pilot__profile')

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pilot__profile=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class FlightViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = FlightSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        defaults = dict()
        fsuipc_data = request.data.get('fsuipc_data')
        defaults['penalty'] = set()
        penalties = Penalty.objects.all()
        if book := Book.objects.filter(id=fsuipc_data.get('book')).first():
            defaults['company'] = book.company.id if getattr(book, 'company') else None
            defaults['flightnum'] = book.schedule.flightnum if getattr(book, 'schedule') else None
            defaults['callsign'] = book.callsign if getattr(book, 'callsign') else None
            defaults['aircraft_type'] = book.aircraft.aircraft_type.aircraft_name if getattr(book, 'aircraft') else None
            defaults['aircraft_registration'] = book.aircraft.aircraft_registration if getattr(book, 'aircraft') else None
            defaults['departure_airport'] = book.dep_airport.id if getattr(book, 'dep_airport') else None
            defaults['arrival_airport'] = book.arr_airport.id if getattr(book, 'arr_airport') else None
            #     hub
            if (penalty := penalties.filter(name='Bonus for return to hub').first()) and book.arr_airport.icao_code == book.company.hub:
                defaults['penalty'].add(penalty)
            defaults['route'] = book.route if getattr(book, 'route') else None
            defaults['pax'] = book.pax if getattr(book, 'pax') else None
            defaults['cargo'] = book.pax if getattr(book, 'cargo') else None
        defaults['distance'] = fsuipc_data.get('distance_flown', 0)
        #     Distance
        if (penalty := penalties.filter(name='Bonus Long Flight 1200-1800').first()) and 1200 < defaults['distance'] < 1800:
            defaults['penalty'].add(penalty)
        elif (penalty := penalties.filter(name='Bonus Long Flight 1800-3600').first()) and 1800 < defaults['distance'] < 3600:
            defaults['penalty'].add(penalty)
        elif (penalty := penalties.filter(name='Bonus Long Flight >3600').first()) and defaults['distance'] > 3600:
            defaults['penalty'].add(penalty)
        #     Crash
        if (penalty := penalties.filter(name='Crash').first()) and fsuipc_data.get('crash'):
            defaults['penalty'].add(penalty)
        #     Stall
        if (penalty := penalties.filter(name='Stall penalty').first()) and fsuipc_data.get('stall'):
            defaults['penalty'].add(penalty)
        #     Overspeed penalty
        if (penalty := penalties.filter(name='Overspeed penalty').first()) and fsuipc_data.get('overspeed'):
            defaults['penalty'].add(penalty)
        #     Landings
        if (penalty := penalties.filter(name='Bonus for perfect landing').first()) and -240 < fsuipc_data.get('landing_vs', 0) < -80:
            defaults['penalty'].add(penalty)
        elif (penalty := penalties.filter(name='Hard Landing Penalty').first()) and -700 < fsuipc_data.get('landing_vs', 0) < -500:
            defaults['penalty'].add(penalty)
        elif (penalty := penalties.filter(name='Emergency Landing Penalty').first()) and -1600 < fsuipc_data.get('landing_vs', 0) < -700:
            defaults['penalty'].add(penalty)
        elif (penalty := penalties.filter(name='Crash').first()) and -1600 > fsuipc_data.get('landing_vs', 0):
            defaults['penalty'].add(penalty)
        defaults['points'] = 100
        defaults['fuel_used'] = fsuipc_data.get('dep_fuel', 0) - fsuipc_data.get('fuel', 0)
        defaults['fuel_left'] = fsuipc_data.get('fuel', 0)
        defaults['zfw'] = fsuipc_data.get('zfw', 0)
        defaults['to_weight'] = fsuipc_data.get('dep_tw', 0)
        defaults['landing_weight'] = fsuipc_data.get('tw', 0)
        defaults['pilot'] = self.request.user.pilot.id
        for pen in defaults['penalty']:
            defaults['points'] += pen.rate
        defaults['penalty'] = [pen.id for pen in defaults['penalty']]
        serializer = self.get_serializer(data={**request.data, **defaults, **fsuipc_data})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
