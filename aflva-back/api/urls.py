from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import BookViewSet, FlightViewSet, StatsViewSet

router = SimpleRouter()
router.register(r'books', BookViewSet, basename='books')
router.register(r'flights', FlightViewSet, basename='flights')
router.register(r'stats', StatsViewSet, basename='stats')

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]

urlpatterns += router.urls
