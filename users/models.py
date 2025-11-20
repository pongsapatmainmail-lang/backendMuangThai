from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="อีเมล")
    phone = models.CharField(max_length=20, blank=True, verbose_name="เบอร์โทร")
    address = models.TextField(blank=True, verbose_name="ที่อยู่")
    is_admin = models.BooleanField(default=False, verbose_name="ผู้ดูแลระบบ")
    
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = "ผู้ใช้"
        verbose_name_plural = "ผู้ใช้"