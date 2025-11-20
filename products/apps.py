from django.apps import AppConfig

class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'

    def ready(self):
        # เรียกใช้ superuser creation ตอน app พร้อม
        from .createsuperuser_on_startup import create_default_superuser
        try:
            create_default_superuser()
        except Exception as e:
            # ป้องกันปัญหา db ยังไม่พร้อม
            print(f"Superuser creation skipped: {e}")
