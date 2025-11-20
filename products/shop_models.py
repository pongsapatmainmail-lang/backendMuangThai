from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Shop(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shops', verbose_name="เจ้าของร้าน")
    name = models.CharField(max_length=200, verbose_name="ชื่อร้าน")
    description = models.TextField(blank=True, verbose_name="คำอธิบาย")
    logo = models.ImageField(upload_to='shops/', null=True, blank=True, verbose_name="โลโก้ร้าน")
    banner = models.ImageField(upload_to='shops/banners/', null=True, blank=True, verbose_name="แบนเนอร์")
    
    # ข้อมูลการติดต่อ
    phone = models.CharField(max_length=20, blank=True, verbose_name="เบอร์โทร")
    email = models.EmailField(blank=True, verbose_name="อีเมล")
    address = models.TextField(blank=True, verbose_name="ที่อยู่")
    
    # สถานะ
    is_active = models.BooleanField(default=True, verbose_name="เปิดใช้งาน")
    is_verified = models.BooleanField(default=False, verbose_name="ยืนยันแล้ว")
    
    # วันที่
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="วันที่สร้าง")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="วันที่แก้ไข")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "ร้านค้า"
        verbose_name_plural = "ร้านค้า"
        ordering = ['-created_at']

    def get_total_products(self):
        return self.products.count()

    def get_total_sales(self):
        from orders.models import OrderItem
        return OrderItem.objects.filter(
            product__shop=self,
            order__status__in=['delivered', 'shipped', 'processing']
        ).count()