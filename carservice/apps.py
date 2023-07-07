from django.apps import AppConfig


class CarserviceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'carservice'

    def ready(self):
        from .tasks import update_rent_status
        update_rent_status()
