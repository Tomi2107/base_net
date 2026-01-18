from django.apps import AppConfig


class FosterConfig(AppConfig):
    name = 'foster'

    def ready(self):
        import foster.signals
        
