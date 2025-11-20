from django.contrib.auth import get_user_model

def create_default_superuser():
    """
    สร้าง superuser โดยตรวจสอบก่อนว่ามีอยู่แล้วหรือไม่
    """
    User = get_user_model()
    username = "admin"
    email = "admin@example.com"
    password = "admin123"

    if not User.objects.filter(email=email).exists():
        print("Creating default superuser...")
        User.objects.create_superuser(username=username, email=email, password=password)
    else:
        print("Superuser already exists.")
