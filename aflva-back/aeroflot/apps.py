from django.apps import AppConfig


class AeroflotConfig(AppConfig):
    name = 'aeroflot'

    def ready(self):
        import aeroflot.signals
