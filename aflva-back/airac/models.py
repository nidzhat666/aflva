from django.db import models
from django_countries.fields import CountryField


# Create your models here.

class Airport(models.Model):
    icao_code = models.CharField(max_length=4, unique=True)
    iata_code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = CountryField(verbose_name='Country')
    elevation = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.icao_code + " - " + self.city + " - " + self.name

    def save(self, force_insert=False, force_update=False):
        self.icao_code = self.icao_code.upper()
        self.iata_code = self.iata_code.upper()
        super(Airport, self).save(force_insert, force_update)
