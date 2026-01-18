from django.apps import AppConfig


class LostFoundConfig(AppConfig):
    name = 'lost_found'

    def ready(self):
        import lost_found.signals
        
