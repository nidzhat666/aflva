# Generated by Django 3.2.6 on 2022-05-23 18:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('aeroflot', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pilot',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pilot', to=settings.AUTH_USER_MODEL, verbose_name='Pilot'),
        ),
    ]
