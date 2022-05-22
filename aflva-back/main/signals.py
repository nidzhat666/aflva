from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import Profile

User = get_user_model()


@receiver(post_save, sender=User)
def flight_post_save(sender, **kwargs):
    instance = kwargs.get('instance')
    print('signal!!')
    Profile.objects.get_or_create(
        user=instance
    )
