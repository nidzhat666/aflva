from .models import Schedule, Fleet


def check_fleet_avail():
    schedules = Schedule.objects.all()
    for schedule in schedules:
        schedule.flightnum
