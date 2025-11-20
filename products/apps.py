from django.apps import AppConfig

class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'

    def ready(self):
        from .createsuperuser_on_startup import create_default_superuser
        create_default_superuser()
