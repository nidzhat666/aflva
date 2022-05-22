from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from .views import BookViewSet, FlightViewSet

router = SimpleRouter()
router.register(r'books', BookViewSet, basename='books')
router.register(r'flights', FlightViewSet, basename='flights')

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]

urlpatterns += router.urls
