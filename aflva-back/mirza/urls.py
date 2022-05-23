from django.contrib import admin
from django.urls import path, include, re_path
from main.views import get_apt_data, book_api, ObtainAuthToken, user_api, delete_booking_api, flight_upload, \
    get_agent_api, book_status_api
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="AFL VA API",
        default_version='v1',
        description="None",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="nagalarov@mail.ru"),
        license=openapi.License(name="BSD License"),
        urlconf='api.urls'
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
                  path('api/', include('api.urls')),
                  path('api-auth/', include('rest_framework.urls')),
                  path('api-agent/', get_agent_api, name='get_agent_api'),
                  path('api-book/', book_api, name='book_api'),
                  path('api-book-status/', book_status_api, name='book_status_api'),
                  path('api-delete-booking/', delete_booking_api, name='delete_booking_api'),
                  path('api-flight-upload/', flight_upload, name='flight_upload'),
                  path('api-user/', user_api, name='user_api'),
                  path('api-token-auth/', ObtainAuthToken.as_view(), name='api_token_auth'),
                  path('', include(('aeroflot.urls', 'aeroflot'), namespace='aeroflot')),
                  path('admin/', admin.site.urls),
                  path('get_apt_info/', get_apt_data, name='get_apt_data'),
                  path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
              ]
# urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
