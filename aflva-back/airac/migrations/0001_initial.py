# Generated by Django 3.2.6 on 2022-02-06 18:24

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icao_code', models.CharField(max_length=4, unique=True)),
                ('iata_code', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('country', django_countries.fields.CountryField(max_length=2, verbose_name='Country')),
                ('elevation', models.IntegerField()),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
        ),
    ]
