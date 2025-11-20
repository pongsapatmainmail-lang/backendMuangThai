from django.contrib.auth import get_user_model

User = get_user_model()

def create_default_superuser():
    username = "adminken"
    email = "adminkenjin@gmail.com"
    password = "280440Ken@"

    # สร้างเฉพาะถ้ายังไม่มี
    if not User.objects.filter(email=email).exists():
        print("Creating default superuser...")
        User.objects.create_superuser(username=username, email=email, password=password)
    else:
        print("Superuser already exists. Skipping creation.")
