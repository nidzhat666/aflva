from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated

from aeroflot.models import Book, Flight
from main.serializers import BookSerializer
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
    queryset = Flight.objects.all()
