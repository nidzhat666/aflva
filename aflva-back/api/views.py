from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from aeroflot.models import Book
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
        if book := Book.objects.filter(id=fsuipc_data.get('book')).first():
            defaults['company'] = book.company.id if getattr(book, 'company') else None
            defaults['flightnum'] = book.schedule.flightnum if getattr(book, 'schedule') else None
            defaults['callsign'] = book.callsign if getattr(book, 'callsign') else None
            defaults['aircraft_type'] = book.aircraft.aircraft_type.aircraft_name if getattr(book, 'aircraft') else None
            defaults['aircraft_registration'] = book.aircraft.aircraft_registration if getattr(book, 'aircraft') else None
            defaults['departure_airport'] = book.dep_airport.id if getattr(book, 'dep_airport') else None
            defaults['arrival_airport'] = book.arr_airport.id if getattr(book, 'arr_airport') else None
            defaults['route'] = book.route if getattr(book, 'route') else None
            defaults['pax'] = book.pax if getattr(book, 'pax') else None
            defaults['cargo'] = book.pax if getattr(book, 'cargo') else None
        defaults['dep_time'] = fsuipc_data.get('dep_time')
        defaults['arr_time'] = fsuipc_data.get('arr_time')
        defaults['flight_time'] = fsuipc_data.get('flight_time')
        defaults['distance'] = fsuipc_data.get('distance_flown')
        defaults['landing_vs'] = fsuipc_data.get('landing_vs')
        defaults['points'] = 120
        defaults['fuel_used'] = fsuipc_data.get('dep_fuel') - fsuipc_data.get('fuel') \
            if isinstance(fsuipc_data.get('dep_fuel'), int) and isinstance(fsuipc_data.get('fuel'), int) else None
        defaults['fuel_left'] = fsuipc_data.get('fuel')
        defaults['zfw'] = fsuipc_data.get('zfw')
        defaults['to_weight'] = fsuipc_data.get('dep_tw')
        defaults['landing_weight'] = fsuipc_data.get('tw')
        defaults['pilot'] = self.request.user.pilot.id
        serializer = self.get_serializer(data={**request.data, **defaults})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
