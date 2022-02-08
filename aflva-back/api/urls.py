from rest_framework.routers import SimpleRouter

from .views import BookViewSet, FlightViewSet


router = SimpleRouter()
router.register(r'books', BookViewSet, basename='books')
router.register(r'flights', FlightViewSet, basename='flights')

urlpatterns = router.urls

