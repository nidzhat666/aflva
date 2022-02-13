from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Flight, Fleet


# @receiver(pre_save, sender=Flight)
# def flight_pre_save(sender, instance, *args, **kwargs):
#     print('signal0')
#     instance.flight_number = 'SU123'
#     return instance


@receiver(post_save, sender=Flight)
def flight_post_save(sender, **kwargs):
    instance = kwargs.get('instance')
    if instance.arrival_airport and (obj := Fleet.objects.filter(aircraft_registration=instance.aircraft_registration).first()):
        obj.now = instance.arrival_airport
        obj.save()
    if hasattr(instance.pilot, 'book'):
        instance.pilot.book.delete()
