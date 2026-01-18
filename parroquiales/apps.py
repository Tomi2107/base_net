from django.apps import AppConfig


class ParroquialesConfig(AppConfig):
    name = 'parroquiales'

    def ready(self):
        import parroquiales.signals
        
