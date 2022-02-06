import datetime

import telebot
from dateutil.relativedelta import relativedelta
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.db.models import Count, Avg, Sum
from django.db.models import IntegerField
from django.db.models import Prefetch
from django.db.models.functions import Cast
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from airac.scripts import add_check_airport
from main.models import Profile, AircraftICAO
from main.serializers import BookSerializer
from .models import AircraftImage, Fleet, Schedule, Pilot, Book, Flight, News

MONTHS = {
    1: ('Январь', 'January'),
    2: ('Февраль', 'February'),
    3: ('Март', 'March'),
    4: ('Апрель', 'April'),
    5: ('Май', 'May'),
    6: ('Июнь', 'June'),
    7: ('Июль', 'July'),
    8: ('Август', 'August'),
    9: ('Сентябрь', 'September'),
    10: ('Октябрь', 'October'),
    11: ('Ноябрь', 'November'),
    12: ('Декабрь', 'December'),
}


def auth_check(func):
    def function(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('aeroflot:login')
        if Pilot.objects.select_related('profile').filter(profile=request.user.id, status='Active'):
            pass
        else:
            return redirect('aeroflot:wait')
        return func(request, *args, **kwargs)

    return function


def return_lang(*args):
    if args[0].GET.get('lang') == 'ru':
        args[0].session['lang'] = 'ru'
        return render(*args)
    elif (args[0].session.get('lang') == 'en') or (args[0].GET.get('lang') == 'en'):
        args[0].session['lang'] = 'en'
        args = list(args)
        args[1] = args[1].split('/')
        args[1].insert(-1, 'en')
        args[1] = '/'.join(args[1])
        return render(*args)
    else:
        args[0].session['lang'] = 'ru'
        return render(*args)


@auth_check
def get_bookings(request):
    book = Book.objects.all().order_by('company__name', 'id').select_related('dep_airport',
                                                                             'arr_airport',
                                                                             'alternate_airport',
                                                                             'pilot',
                                                                             'pilot__profile',
                                                                             'aircraft',
                                                                             'aircraft__aircraft_type',
                                                                             'aircraft__aircraft_type__aircraft_icao',
                                                                             'company', )
    serializer = BookSerializer(book, many=True)
    return JsonResponse(serializer.data, safe=False)


@auth_check
def main(request):
    prev_month = (datetime.datetime.now() - relativedelta(months=1)).month
    top_pilots = Pilot.objects.filter(flight__dep_time__month=prev_month).select_related('profile') \
                     .prefetch_related('flight') \
                     .annotate(flight_count=Count('flight'),
                               average_rating=Cast(Avg('flight__points'), IntegerField())) \
                     .filter(flight_count__gt=5) \
                     .order_by('-flight_count', '-average_rating')[:5]
    pilots_overall = Pilot.objects.all().aggregate(count=Count('id'),
                                                   additional_hours=Sum('additional_hours'),
                                                   additional_flights=Sum('additional_flights'))
    flight_stat = Flight.objects.all().aggregate(count=pilots_overall.get('additional_flights') + Count('id'),
                                                 hours=pilots_overall.get('additional_hours') + Sum('flight_time'))
    fleet_stat = Fleet.objects.all().aggregate(count=Count('id'))
    flights = Flight.objects.all().select_related('departure_airport',
                                                  'arrival_airport',
                                                  'pilot',
                                                  'pilot__profile',
                                                  'company').order_by('-id')[:100]
    news = News.objects.all().order_by('-id')
    return return_lang(request, 'aeroflot/index.html', {'top_pilots': top_pilots,
                                                        'pilots_overall': pilots_overall,
                                                        'flight_stat': flight_stat,
                                                        'prev_month': prev_month,
                                                        'last_month': MONTHS[prev_month],
                                                        'flights': flights,
                                                        'fleet_stat': fleet_stat, 'news': news})


@auth_check
def crew(request):
    crew = Pilot.objects.filter(status='Active').order_by('callsign') \
        .select_related('profile', 'profile__profile') \
        .prefetch_related('flight')
    return return_lang(request, 'aeroflot/crew.html', {'crew': crew})


@auth_check
def pilot(request, callsign):
    pilot = Pilot.objects.get(callsign=callsign.upper())
    user = User.objects.get(id=pilot.profile.id)
    profile = Profile.objects.get(user=user)
    flights = Flight.objects.filter(pilot=pilot).order_by('-id')
    flown_aircraft = {}
    flown_countries = {}
    fa = {}
    for i in flights:
        if not flown_aircraft.get(i.aircraft_type):
            flown_aircraft[i.aircraft_type] = 1
        else:
            flown_aircraft[i.aircraft_type] += 1
        if not flown_countries.get((i.arrival_airport.country.code, i.arrival_airport.icao_code)):
            flown_countries[(i.arrival_airport.country.code, i.arrival_airport.icao_code)] = 1
        else:
            flown_countries[(i.arrival_airport.country.code, i.arrival_airport.icao_code)] += 1
        if not fa.get(i.dep_time.month):
            fa[i.dep_time.month] = 1
        else:
            fa[i.dep_time.month] += 1
    fa1 = [i for i in fa.items()]
    fa1.sort(key=lambda x: x[0], reverse=False)
    flown_countries1 = [i for i in flown_countries.items()]
    flown_countries1.sort(key=lambda x: x[-1], reverse=True)
    flown_aircraft1 = [i for i in flown_aircraft.items()]
    flown_aircraft1.sort(key=lambda x: x[-1], reverse=True)
    return return_lang(request, 'aeroflot/pilot.html', {
        'flown_countries': flown_countries1[:8],
        'flown_aircraft': flown_aircraft1[:8],
        'month_names': MONTHS,
        'fa': fa1[:12],
        'pilot': pilot,
        'profile': profile,
        'flights': flights
    })


@auth_check
def fleet(request):
    schedule = None
    fleet_filter = {'status': 'Active'}
    schedule_filter = {'status': 'Active'}
    req = request.GET
    if req.get('company'):
        fleet_filter['company__name'] = req.get('company')
        schedule_filter['company__name'] = req.get('company')
    if req.get('s_id'):
        schedule = get_object_or_404(Schedule, id=req.get('s_id'))
        fleet_filter['aircraft_type__aircraft_icao__aircraft_image__company'] = schedule.company
        fleet_filter['aircraft_type__aircraft_icao__in'] = schedule.aircraft_type.all()
        fleet_filter['now'] = schedule.dep_icao
    elif req.get('type') == 'Retro':
        fleet_filter['status'] = 'Retro'
    elif req.get('type') == 'Charter':
        del fleet_filter['status']
        fleet_filter['status__in'] = ('Retro', 'Active')
    if req.get('company'):
        fleet_filter['aircraft_type__aircraft_icao__aircraft_image__company__name'] = req.get('company')
    fleet = Fleet.objects.select_related('company', 'now', 'aircraft_type__aircraft_icao',
                                         'book')
    fleet = fleet.filter(**fleet_filter).order_by('aircraft_type__aircraft_name', 'aircraft_registration')
    icao = fleet.values_list('aircraft_type__aircraft_icao__aircraft_icao',
                             'aircraft_type__aircraft_icao__aircraft_image__aircraft_image').distinct() \
        .order_by('-status', 'aircraft_type__aircraft_icao__aircraft_icao')
    schedule_avail = Schedule.objects.select_related('dep_icao', 'book', 'company') \
        .prefetch_related('aircraft_type', 'aircraft_type__aircraft_icao')
    schedule_avail = schedule_avail.filter(**schedule_filter).values_list('dep_icao__icao_code',
                                                                          'aircraft_type__aircraft_icao',
                                                                          'book__status', ).distinct()
    return return_lang(request, 'aeroflot/fleet.html', {'fleets': fleet,
                                                        'schedule': schedule,
                                                        'icaos': icao,
                                                        'schedule_avail': schedule_avail})


@auth_check
def aircraft_details(request, registration):
    aircraft = Fleet.objects.get(aircraft_registration=registration)
    flights = Flight.objects.filter(aircraft_registration=aircraft.aircraft_registration).order_by('-id')
    if not aircraft.aircraft_image:
        aircraft_image = AircraftImage.objects.filter(company=aircraft.company,
                                                      aircraft_icao=aircraft.aircraft_type.aircraft_icao)
        return return_lang(request, 'aeroflot/aircraft_details.html',
                           {'aircraft': aircraft, 'aircraft_icao_image': aircraft_image, 'flights': flights})
    return return_lang(request, 'aeroflot/aircraft_details.html', {'aircraft': aircraft, 'flights': flights})


def fleet_to_dict(query):
    fleet = {}
    for i in query:
        icao = i.get('aircraft_type__aircraft_icao__aircraft_icao')
        now = i.get('now__icao_code')
        company = i.get('company')
        key = (icao, now, company)
        status = i.get('book__status')
        if fleet.get((icao, now, company)):
            fleet[key].add(status)
        else:
            fleet[key] = {status}
    return fleet


@auth_check
def schedules(request):
    aircraft = None
    schedules_filters = {'status': 'Active'}
    fleet_filters = {}
    req = request.GET
    if request.GET.get('f_id'):
        aircraft = Fleet.objects.select_related('aircraft_type__aircraft_icao').get(id=request.GET.get('f_id'))
        schedules_filters['company'] = aircraft.company
    if req.get('company'):
        schedules_filters['company__name'] = req.get('company')
        fleet_filters['company__name__iexact'] = req.get('company')
    if req.get('origin'):
        schedules_filters['dep_icao__icao_code__iexact'] = req.get('origin')
    if req.get('dest'):
        schedules_filters['arr_icao__icao_code__iexact'] = req.get('dest')
    if aircraft:
        schedules_filters['dep_icao'] = aircraft.now
        schedules_filters['aircraft_type'] = aircraft.aircraft_type.aircraft_icao
    schedule = Schedule.objects.select_related('arr_icao', 'dep_icao', 'company') \
        .prefetch_related('book', 'aircraft_type') \
        .filter(**schedules_filters).order_by('flightnum')
    fleet = Fleet.objects.prefetch_related(Prefetch('aircraft_type__aircraft_icao__aircraft_icao'
                                                    , AircraftICAO.objects.all().only('')),
                                           'aircraft_type__aircraft_icao',
                                           'book') \
        .filter(**fleet_filters) \
        .select_related('now') \
        .values('aircraft_type__aircraft_icao__aircraft_icao', 'now__icao_code', 'book__status', 'company').distinct()
    fleet = fleet_to_dict(fleet)
    return return_lang(request, 'aeroflot/schedules.html', {'schedules': schedule,
                                                            'fleet': fleet, 'aircraft': aircraft})


@auth_check
def prebook(request):
    if request.method == 'POST':
        schedule = request.POST.get('schedule')
        aircraft = request.POST.get('aircraft')
        fleet = Fleet.objects.get(id=aircraft)
        if request.POST.get('charter'):
            return return_lang(request, 'aeroflot/prebook_charter.html', {'fleet': fleet})
        schedule = Schedule.objects.get(id=schedule)
    return return_lang(request, 'aeroflot/prebook.html', {'schedule': schedule, 'fleet': fleet})


@auth_check
def flight_view(request):
    req = request.POST
    flight = Flight.objects.get(id=req.get('flight_id'))
    aircraft = Fleet.objects.filter(aircraft_registration=flight.aircraft_registration)
    penalty = flight.penalty.all().order_by('rate')
    return return_lang(request, 'aeroflot/flight_view.html',
                       {'flight': flight, 'aircraft': aircraft, 'penalty': penalty})


@auth_check
def booking(request):
    if request.method == "POST":
        import datetime
        req = request.POST
        book = Book()
        schedule = Schedule.objects.get(id=req.get('schedule'))
        schedule_fleet = [i for i in schedule.aircraft_type.all()]
        if Book.objects.filter(schedule=schedule):
            return return_lang(request, 'aeroflot/error.html', {'error': 'This flight has been already booked.'})
        fleet = Fleet.objects.get(id=req.get('fleet'))
        if fleet.aircraft_type.aircraft_icao not in schedule_fleet:
            return return_lang(request, 'aeroflot/error.html',
                               {'error': 'This aircraft not supperted for this flight.'})
        if Book.objects.filter(aircraft=fleet):
            return return_lang(request, 'aeroflot/error.html', {'error': 'This aircraft has been already booked.'})
        pilot = Pilot.objects.get(profile=User.objects.get(id=request.user.id))
        if Book.objects.filter(pilot=pilot):
            return return_lang(request, 'aeroflot/error.html', {'error': 'You already have a booking'})
        book.schedule = schedule
        book.pilot = pilot
        book.company = schedule.company
        book.aircraft = fleet
        book.callsign = schedule.callsign
        book.dep_airport = schedule.dep_icao
        book.arr_airport = schedule.arr_icao
        apt = add_check_airport(req.get('altrn'))
        if apt:
            book.alternate_airport = add_check_airport(req.get('altrn'))
        else:
            return return_lang(request, 'aeroflot/error.html',
                               {'error': 'Airport ' + req.get('altrn').upper() + ' doesn\'t exist'})
        book.route = req.get('route')
        book.flight_level = req.get('flight_level')
        book.distance = schedule.distance
        book.deptime = datetime.datetime.strptime(
            str(req.get('deptime')), "%H%M").strftime("%H:%M")
        from main.scripts import time_calc
        book.flight_time = time_calc(schedule.deptime, schedule.arrtime)
        book.status = 'booked'
        book.flight_type = 'regular'
        book.pax = req.get('pax')
        book.cargo = req.get('cargo')
        book.save()
    return redirect('aeroflot:profile')


@auth_check
def charter_booking(request):
    if request.method == "POST":
        import datetime
        req = request.POST
        book = Book()
        fleet = Fleet.objects.get(id=req.get('fleet'))
        if Book.objects.filter(aircraft=fleet):
            return return_lang(request, 'aeroflot/error.html', {'error': 'This aircraft has been already booked.'})
        pilot = Pilot.objects.get(profile=User.objects.get(id=request.user.id))
        if Book.objects.filter(pilot=pilot):
            return return_lang(request, 'aeroflot/error.html', {'error': 'You already have a booking'})
        book.pilot = pilot
        book.aircraft = fleet
        book.company = fleet.company
        book.callsign = fleet.company.icao + pilot.callsign
        book.dep_airport = fleet.now
        apt = add_check_airport(req.get('arrapt'))
        if apt:
            book.arr_airport = add_check_airport(req.get('arrapt'))
        else:
            return return_lang(request, 'aeroflot/error.html',
                               {'error': 'Airport ' + req.get('arrapt').upper() + ' doesn\'t exist'})
        apt = add_check_airport(req.get('altrn'))
        if apt:
            book.alternate_airport = add_check_airport(req.get('altrn'))
        else:
            return return_lang(request, 'aeroflot/error.html',
                               {'error': 'Airport ' + req.get('altrn').upper() + ' doesn\'t exist'})
        book.route = req.get('route')
        book.flight_level = req.get('flight_level')
        book.distance = req.get('distance')
        book.deptime = datetime.datetime.strptime(
            str(req.get('deptime')), "%H%M").strftime("%H:%M")
        from main.scripts import time_calc
        book.flight_time = datetime.datetime.strptime(
            str(req.get('flight_time')), "%H%M").strftime("%H:%M")
        book.status = 'booked'
        book.flight_type = 'regular'
        book.pax = req.get('pax')
        book.cargo = req.get('cargo')
        book.save()
    return redirect('aeroflot:profile')


@auth_check
def online(request):
    return return_lang(request, 'aeroflot/online.html')


@auth_check
def profile(request):
    pilot = Pilot.objects.get(profile=User.objects.get(id=request.user.id))
    profile = Profile.objects.get(user=User.objects.get(id=request.user.id))
    book = Book.objects.filter(pilot=pilot)
    if book:
        book = book[0]
    flights = Flight.objects.filter(pilot=pilot).order_by('-id')
    flown_aircraft = {}
    flown_countries = {}
    fa = {}
    for i in flights:
        if not flown_aircraft.get(i.aircraft_type):
            flown_aircraft[i.aircraft_type] = 1
        else:
            flown_aircraft[i.aircraft_type] += 1
        if not flown_countries.get((i.arrival_airport.country.code, i.arrival_airport.icao_code)):
            flown_countries[(i.arrival_airport.country.code, i.arrival_airport.icao_code)] = 1
        else:
            flown_countries[(i.arrival_airport.country.code, i.arrival_airport.icao_code)] += 1
        if not fa.get(i.dep_time.month):
            fa[i.dep_time.month] = 1
        else:
            fa[i.dep_time.month] += 1
    fa1 = [i for i in fa.items()]
    fa1.sort(key=lambda x: x[0], reverse=False)
    flown_countries1 = [i for i in flown_countries.items()]
    flown_countries1.sort(key=lambda x: x[-1], reverse=True)
    flown_aircraft1 = [i for i in flown_aircraft.items()]
    flown_aircraft1.sort(key=lambda x: x[-1], reverse=True)
    return return_lang(request, 'aeroflot/profile.html', {
        'flown_countries': flown_countries1[:8],
        'flown_aircraft': flown_aircraft1[:8],
        'month_names': MONTHS,
        'fa': fa1[:12],
        'pilot': pilot,
        'profile': profile,
        'flights': flights,
        'book': book,
    })


@auth_check
def delete_booking(request):
    book = Book.objects.get(pilot=Pilot.objects.get(profile=request.user.id))
    book.delete()
    return redirect('aeroflot:main')


def bot_send_message(message):
    bot = telebot.TeleBot('1623919400:AAGSMYd-AmTYc7geaxgNPwvvmuhylbkkkkc')
    staff = Profile.objects.filter(user__is_staff=True, telegram_chat_id__isnull=False)
    for i in staff:
        bot.send_message(i.telegram_chat_id, text=message)


def request_apply(request):
    text = """New Pilot in Aeroflot\n{} {}\n{}
    """
    if not request.user.is_authenticated:
        return redirect('aeroflot:login')
    pilot = Pilot.objects.filter(profile=request.user)
    user = request.user
    if pilot:
        pilot = pilot[0]
        if pilot.status == 'Active':
            return redirect('aeroflot:main')
        elif pilot.status == 'Inactive':
            pilot.status = 'Just Registred'
            pilot.save()
            bot_send_message(text.format(user.first_name, user.last_name, user.email))
            return redirect('aeroflot:wait')
        else:
            return redirect('aeroflot:main')
    else:
        pilot = Pilot()
        pilot.profile = user
        pilot.callsign = 'NEW'
        pilot.status = 'Just Registred'
        pilot.save()
        bot_send_message(text.format(user.first_name, user.last_name, user.email))
        return redirect('aeroflot:wait')
    return redirect('aeroflot:main')


def login(request):
    if request.user.is_authenticated and Pilot.objects.filter(id=request.user.id):
        return redirect('aeroflot:main')
    elif request.user.is_authenticated:
        return redirect('aeroflot:wait')

    if request.method == "POST":
        req = request.POST
        try:
            user = User.objects.get(email=req.get('email'))
        except:
            return JsonResponse({"error": "error"})
        user = authenticate(username=user.username,
                            password=req.get('password'))
        if user is not None:
            auth_login(request, user=user)
            return redirect('aeroflot:main')
        else:
            return JsonResponse({"error": "error"})
    return return_lang(request, 'aeroflot/login.html')


def wait(request):
    state = ""
    if request.user.is_authenticated and Pilot.objects.filter(profile=request.user.id, status='Active'):
        return redirect('aeroflot:main')
    elif not request.user.is_authenticated:
        return redirect('aeroflot:login')
    elif Pilot.objects.filter(profile=request.user.id, status='Inactive'):
        state = 'needs to activate'
    elif not Pilot.objects.filter(profile=request.user.id):
        state = 'just registred'
    elif Pilot.objects.filter(profile=request.user.id, status='Just Registred'):
        state = 'waiting'

    return return_lang(request, 'aeroflot/wait.html', {"state": state})


def signup(request):
    import threading
    from django.utils.crypto import get_random_string
    if request.user.is_authenticated and Pilot.objects.filter(id=request.user.id):
        return redirect('aeroflot:main')
    elif request.user.is_authenticated:
        return redirect('aeroflot:wait')
    elif request.method == 'POST':
        req = request.POST
        error = {'error': []}
        if User.objects.filter(email=req.get('email')):
            error['error'].append('email')
        if req.get('vatsim_id'):
            if Profile.objects.filter(vatsimid=req.get('vatsim_id')):
                error['error'].append('vatsim_id')
        if req.get('ivao_id'):
            if Profile.objects.filter(ivaoid=req.get('ivao_id')):
                error['error'].append('ivao_id')
        if error['error']:
            return JsonResponse(error)
        user = User()
        profile = Profile()
        ts = str(int(datetime.datetime.now().timestamp()))
        user.username = req.get('first_name') + req.get('last_name') + ts
        user.first_name = req.get('first_name')
        user.last_name = req.get('last_name')
        user.email = req.get('email')
        password = get_random_string(length=32)
        user.set_password(password)
        user.save()
        profile.user = user
        profile.location = req.get('country')
        if req.get('vatsim_id'):
            profile.vatsimid = req.get('vatsim_id')
        if req.get('ivao_id'):
            profile.ivaoid = req.get('ivao_id')
        profile.now = 'UUEE'
        profile.save()
        t = threading.Thread(target=password_email, args=[req.get('email'), req.get('first_name'), password])
        t.setDaemon(True)
        t.start()
        return JsonResponse({'success': 'success'})
    return return_lang(request, 'aeroflot/signup.html')


def reset_password(request):
    if request.user.is_authenticated and request.method == 'POST':
        user = request.user
        req = request.POST
        if req.get('password'):
            user.set_password(req.get('password'))
            user.save()
            return JsonResponse({"success": "success"})
    elif not request.user.is_authenticated and request.method == 'POST':
        req = request.POST
        user = User.objects.filter(email=req.get('email'))
        if user:
            user = user[0]
            if Profile.objects.filter(user=user, vatsimid=req.get('vatsim')) \
                    or Profile.objects.filter(user=user, ivaoid=req.get('vatsim')):
                import threading
                from django.utils.crypto import get_random_string
                password = get_random_string(length=32)
                user.set_password(password)
                user.save()
                t = threading.Thread(target=password_email, args=[req.get('email'), user.first_name, password])
                t.setDaemon(True)
                t.start()
                return JsonResponse({"success": "success"})
    return JsonResponse({"error": "error"})


def password_email(email, fisrt_name, password):
    from django.core.mail import send_mail
    from django.conf import settings
    send_mail('New Registration',
              f'{fisrt_name} ,welcome to Aeroflot Virtual Airlines.\n\n Your new password: \n{password}',
              settings.EMAIL_HOST_USER,
              [email],
              fail_silently=False,
              )


def contact_us(request):
    if request.user.is_authenticated and request.method == 'POST':
        bot_send_message(
            f"‼️New Email‼️\nName: {request.user.first_name} {request.user.last_name}\nEmail: {request.user.email}\nText:\n{request.POST.get('text')}")
        return JsonResponse({"success": "success"})


def logout(request):
    auth_logout(request)
    return redirect('aeroflot:login')
