# products/createsuperuser_on_startup.py
from django.contrib.auth import get_user_model

User = get_user_model()

def create_default_superuser():
    username = "adminkenjinxxx"
    email = "adminkenjin@example.com"
    password = "280440Ken@"  # ตั้งรหัสผ่านใหม่ทุกครั้ง

    user_qs = User.objects.filter(username=username)
    if not user_qs.exists():
        print("Creating default superuser...")
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            is_staff=True,
            is_active=True,
            is_superuser=True
        )
        print(f"Superuser '{username}' created with password: {password}")
    else:
        user = user_qs.first()
        updated = False
        # ตรวจสอบและแก้ไขสิทธิ์
        if not user.is_staff:
            user.is_staff = True
            updated = True
        if not user.is_superuser:
            user.is_superuser = True
            updated = True
        if not user.is_active:
            user.is_active = True
            updated = True
        # Reset password
        user.set_password(password)
        updated = True
        if updated:
            user.save()
            print(f"Updated superuser '{username}' and reset password to: {password}")
