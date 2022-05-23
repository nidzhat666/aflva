# Generated by Django 3.2.6 on 2022-05-23 15:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
        ('airac', '0001_initial'),
        ('aeroflot', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='aircraft_type',
            field=models.ManyToManyField(to='main.AircraftICAO'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='alternate_icao',
            field=models.ForeignKey(help_text='Example: UUEE', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='alternate_icao', to='airac.airport', verbose_name='Alternative Airport'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='arr_icao',
            field=models.ForeignKey(help_text='Example: UUEE', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='arr_icao', to='airac.airport', verbose_name='Arrival Airport'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='aeroflot.company'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='dep_icao',
            field=models.ForeignKey(help_text='Example: UUEE', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='dep_icao', to='airac.airport', verbose_name='Departure Airport'),
        ),
        migrations.AddField(
            model_name='pilot',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Pilot'),
        ),
        migrations.AddField(
            model_name='flight',
            name='arrival_airport',
            field=models.ForeignKey(blank=True, help_text='Example: UUEE', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='arrival_airport', to='airac.airport', verbose_name='Arrival Airport'),
        ),
        migrations.AddField(
            model_name='flight',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='aeroflot.company'),
        ),
        migrations.AddField(
            model_name='flight',
            name='departure_airport',
            field=models.ForeignKey(blank=True, help_text='Example: UUEE', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='departure_airport', to='airac.airport', verbose_name='Departure Airport'),
        ),
        migrations.AddField(
            model_name='flight',
            name='penalty',
            field=models.ManyToManyField(blank=True, to='main.Penalty'),
        ),
        migrations.AddField(
            model_name='flight',
            name='pilot',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='flight', to='aeroflot.pilot'),
        ),
        migrations.AddField(
            model_name='flight',
            name='sim_version',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='main.simversion'),
        ),
        migrations.AddField(
            model_name='fleet',
            name='aircraft_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fleet', to='main.aircrafttype'),
        ),
        migrations.AddField(
            model_name='fleet',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='fleet', to='aeroflot.company'),
        ),
        migrations.AddField(
            model_name='fleet',
            name='now',
            field=models.ForeignKey(help_text='Example: UUEE', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='fleet', to='airac.airport'),
        ),
        migrations.AddField(
            model_name='book',
            name='aircraft',
            field=models.OneToOneField(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='book', to='aeroflot.fleet'),
        ),
        migrations.AddField(
            model_name='book',
            name='alternate_airport',
            field=models.ForeignKey(editable=False, help_text='Example: UUEE', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='alternate_icao_booking', to='airac.airport', verbose_name='Alternative Airport'),
        ),
        migrations.AddField(
            model_name='book',
            name='arr_airport',
            field=models.ForeignKey(editable=False, help_text='Example: UUEE', on_delete=django.db.models.deletion.PROTECT, related_name='arr_airport', to='airac.airport', verbose_name='Arrival Airport'),
        ),
        migrations.AddField(
            model_name='book',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='book', to='aeroflot.company'),
        ),
        migrations.AddField(
            model_name='book',
            name='dep_airport',
            field=models.ForeignKey(editable=False, help_text='Example: UUEE', on_delete=django.db.models.deletion.PROTECT, related_name='dep_airport', to='airac.airport', verbose_name='Departure Airport'),
        ),
        migrations.AddField(
            model_name='book',
            name='pilot',
            field=models.OneToOneField(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='book', to='aeroflot.pilot'),
        ),
        migrations.AddField(
            model_name='book',
            name='schedule',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='book', to='aeroflot.schedule'),
        ),
        migrations.AddField(
            model_name='aircraftimage',
            name='aircraft_icao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aircraft_image', to='main.aircrafticao'),
        ),
        migrations.AddField(
            model_name='aircraftimage',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='aeroflot.company'),
        ),
        migrations.AlterUniqueTogether(
            name='aircraftimage',
            unique_together={('aircraft_icao', 'company')},
        ),
    ]