from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Flight, Fleet


@receiver(post_save, sender=Flight)
def api_call_handler(sender, **kwargs):
    instance = kwargs.get('instance')
    obj = Fleet.objects.filter(aircraft_registration=instance.aircraft_registration).first()
    obj.now = instance.arrival_airport
    obj.save()
