from django.contrib.auth import get_user_model

User = get_user_model()

def create_default_superuser():
    username = "adminkenjin"
    email = "adminjinxken@gmail.com"
    password = "280440jinx@"

    # ตรวจสอบว่ามี user อยู่แล้วหรือยัง
    if not User.objects.filter(username=username).exists() and not User.objects.filter(email=email).exists():
        print("Creating default superuser...")
        User.objects.create_superuser(username=username, email=email, password=password)
    else:
        print("Superuser already exists. Skipping creation.")
