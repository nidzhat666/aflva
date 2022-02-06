from django.urls import path
from aeroflot.views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
                  path('contact_us/', contact_us, name='contact_us'),
                  path('reset_password/', reset_password, name='reset_password'),
                  path('request_apply/', request_apply, name='request_apply'),
                  path('signup/', signup, name='signup'),
                  path('login/', login, name='login'),
                  path('logout/', logout, name='logout'),
                  path('online/', online, name='online'),
                  path('profile/', profile, name='profile'),
                  path('get-bookings/', get_bookings, name='bookings_api'),
                  path('wait-approval/', wait, name='wait'),
                  path('flight_view/', flight_view, name='flight_view'),
                  path('', main, name='main'),
                  path('fleet/', fleet, name='fleet'),
                  path('pilot/<callsign>/', pilot, name='pilot'),
                  path('crew/', crew, name='crew'),
                  path('schedules/', schedules, name='schedules'),
                  path('fleet/detail/<registration>/', aircraft_details, name='aircraft_details'),
                  path('prebook/', prebook, name='prebook'),
                  path('booking/', booking, name='booking'),
                  path('charter_booking/', charter_booking, name='charter_booking'),
                  path('delete_booking/', delete_booking, name='delete_booking'),
              ] + staticfiles_urlpatterns()
