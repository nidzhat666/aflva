from django import template
import datetime, requests
from aeroflot.models import Fleet, Pilot, Book, Schedule, Company
from main.models import Profile
from django.contrib.auth.models import User
from math import floor

register = template.Library()


@register.simple_tag()
def check_schedule(fleet, acf, apt, company):
    for i in acf:
        key = (i.aircraft_icao, apt.icao_code, company)
        # print(key)
        obj = fleet.get(key)
        if obj:
            if None in obj:
                return 'free'
            if 'booked' in obj:
                return 'booked'
    return 'no aircraft'


@register.simple_tag()
def check_fleet(schedule,acf, apt):
    return (apt, acf, None) in list(schedule)



@register.simple_tag()
def check_schedule_deactivated(fleet, acf, apt):
    fleet = fleet.filter(now=apt)
    if fleet:
        fleet = fleet.filter(aircraft_type__aircraft_icao__in=acf)
        if fleet:
            if not None in [i.get('book__status') for i in fleet]:
                return 'booked'
            return 'free'
    return 'no aircraft'


@register.simple_tag()
def time_calc(dep_time, arr_time):
    dateTimeA = datetime.datetime.combine(datetime.date.today(), dep_time)
    dateTimeB = datetime.datetime.combine(datetime.date.today(), arr_time)
    dateTimeDifference = dateTimeB - dateTimeA
    try:
        return datetime.datetime.strptime(str(dateTimeDifference), "%H:%M:%S").strftime("%H:%M")
    except:
        dateTimeDifference = dateTimeDifference + datetime.timedelta(days=1)
        return datetime.datetime.strptime(str(dateTimeDifference), "%H:%M:%S").strftime("%H:%M")


@register.simple_tag()
def weight_calc(fleet, schedule, weight_type):
    if weight_type == 'pax':
        return floor(fleet.aircraft_type.pax / 100 * schedule.payload_percentage)
    elif weight_type == 'cargo':
        return floor(fleet.aircraft_type.payload - (fleet.aircraft_type.pax * 85) / 100 * schedule.payload_percentage)


# @register.simple_tag()
# def aircraft_location_check(icao, aircrafts):
#     for i in 
#     return fleet_check


@register.simple_tag()
def check_pilot(user_id):
    pilot = Pilot.objects.get(profile=user_id)
    return pilot


@register.simple_tag()
def check_book_schedule(id):
    schedule = Schedule.objects.get(id=id)
    book = Book.objects.filter(schedule=schedule)
    if book:
        return book[0].status
    else:
        return True


@register.simple_tag()
def check_book_fleet(id):
    fleet = Fleet.objects.get(id=id)
    book = Book.objects.filter(aircraft=fleet.id)
    if book:
        return book[0].status
    else:
        return True


@register.simple_tag()
def get_metar(code):
    try:
        icao = code
        url = 'https://avwx.rest/api/metar/' + icao
        header = {'Authorization': 'ASZtHjzIsCzdOG--WkML2RlP-QLre9VKCXpLFWu1WIA'}
        res = requests.get(url, headers=header)
        res = res.json()
        return res['raw']
    except:
        return ''


@register.filter(name='convert_hours')
def convert_hours(seconds):
    if seconds:
        hour = seconds // 3600
    else:
        hour = 0
    return hour


@register.filter()
def convert_hours_minutes(seconds):
    # seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (hour, minutes)




@register.filter()
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter()
def get_index(dictionary, key):
    return dictionary[key]


@register.filter()
def get_index_tuple(tup, index):
    return tup[index]


@register.simple_tag()
def vatsim_time(id):
    url = f'https://api.vatsim.net/api/ratings/{id}/'
    req = requests.get(url)
    res = req.json()
    if res.get('reg_date'):
        time1 = datetime.datetime.strptime(res.get('reg_date'), '%Y-%m-%dT%H:%M:%S')
        time1 = time1.strftime('%Y.%m.%d')
        return time1
    return 'Vatsim User Not Found'


@register.simple_tag()
def get_profile(user_id):
    user = User.objects.get(id=user_id)
    profile = Profile.objects.get(user=user)
    return profile


@register.simple_tag()
def get_companies(retro=False):
    if retro:
        companies = Company.objects.filter(fleet__status='Retro').exclude(fleet__isnull=True).order_by('name').distinct()
        return companies
    companies = Company.objects.all()
    return companies


@register.filter()
def icao_to_fleet(fleet, icao):
    return fleet.filter(aircraft_type__aircraft_icao__aircraft_icao=icao)
