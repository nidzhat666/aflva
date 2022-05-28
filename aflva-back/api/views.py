from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.shortcuts import get_object_or_404
from django.db.models import Count, Avg, Sum
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from aeroflot.models import Book, Pilot, Flight, Fleet, Company, Schedule
from main.models import Penalty
from .serializers import (FlightSerializer, BookShortSerializer,
                          PilotTopSerializer, CompanyDedicatedSerializer, ScheduleSerializer)
from .utils import convert_hours


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


class ScheduleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (Schedule.objects.filter(is_active=True)
                .select_related('arr_icao', 'dep_icao', 'alternate_icao', 'company')
                .order_by('flightnum'))
    page_size = 20
    serializer_class = ScheduleSerializer
    permission_classes = (IsAuthenticated,)
    filterset_fields = ('company__name',)
    search_fields = ['dep_icao__icao_code', 'dep_icao__name', 'dep_icao__city',
                     'arr_icao__icao_code', 'arr_icao__name', 'arr_icao__city', 'flightnum']
    ordering_fields = ['dep_icao__icao_code', 'arr_icao__icao_code', 'distance', 'deptime', 'flightnum']


class CompanyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CompanyDedicatedSerializer
    queryset = Company.objects.all()


class StatsViewSet(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=['GET'])
    def overall(self, request):
        pilots_overall = Pilot.objects.all().aggregate(count=Count('id'),
                                                       additional_hours=Sum('additional_hours'),
                                                       additional_flights=Sum('additional_flights'))
        flights_stat = Flight.objects.all().aggregate(count=pilots_overall.get('additional_flights') + Count('id'),
                                                      hours=pilots_overall.get('additional_hours') + Sum('flight_time'))
        flights_stat['hours'] = convert_hours(flights_stat['hours'])
        fleet_stat = Fleet.objects.all().aggregate(count=Count('id'))
        return Response(dict(flights=flights_stat, fleet=fleet_stat, pilots=pilots_overall.get('count')))

    @action(detail=False, methods=['GET'])
    def pilots_top(self, request):
        prev_month = (datetime.now() - relativedelta(months=1)).month
        top_pilots = Pilot.objects.filter(flight__dep_time__month=prev_month, flight__points__isnull=False) \
                         .select_related('profile') \
                         .prefetch_related('flight') \
                         .annotate(flight_count=Count('flight'),
                                   average_rating=Avg('flight__points')) \
                         .filter(flight_count__gt=5) \
                         .order_by('-flight_count', '-average_rating')[:5]
        serializer = PilotTopSerializer(top_pilots, many=True)
        return Response(dict(top=serializer.data, month=prev_month))


class FlightViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = FlightSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        defaults = dict()
        fsuipc_data = request.data.get('fsuipc_data')
        defaults['penalty'] = set()
        penalties = Penalty.objects.all()
        if hasattr(self.request.user.pilot, 'book'):
            book = self.request.user.pilot.book
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
            defaults['cargo'] = book.cargo if getattr(book, 'cargo') else None
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
