from .models import Airport
import requests


def add_check_airport(icao):
    icao = icao.upper()
    try:
        apt = Airport.objects.get(icao_code=icao)
        return apt
    except:
        url = 'https://avwx.rest/api/station/'+icao
        header = {'Authorization':'ASZtHjzIsCzdOG--WkML2RlP-QLre9VKCXpLFWu1WIA'}
        res = requests.get(url, headers=header)
        res = res.json()
        if res.get('error'):
            return 0
        apt = Airport()
        apt.icao_code = res.get('icao')
        apt.iata_code = res.get('iata')
        apt.name = res.get('name')
        apt.city = res.get('city')
        apt.country = res.get('country')
        apt.elevation = res.get('elevation_ft')
        apt.latitude = res.get('latitude')
        apt.longitude = res.get('longitude')
        apt.save()
        return apt