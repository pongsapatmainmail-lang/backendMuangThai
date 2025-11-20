from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'รอดำเนินการ'),
        ('processing', 'กำลังดำเนินการ'),
        ('shipped', 'จัดส่งแล้ว'),
        ('delivered', 'ได้รับสินค้าแล้ว'),
        ('cancelled', 'ยกเลิก'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name="ผู้สั่งซื้อ")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="สถานะ")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="ยอดรวม")
    
    # ข้อมูลการจัดส่ง
    shipping_name = models.CharField(max_length=100, verbose_name="ชื่อผู้รับ")
    shipping_address = models.TextField(verbose_name="ที่อยู่จัดส่ง")
    shipping_phone = models.CharField(max_length=20, verbose_name="เบอร์โทรศัพท์")
    
    # วันที่
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="วันที่สั่งซื้อ")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="วันที่แก้ไข")

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

    class Meta:
        verbose_name = "คำสั่งซื้อ"
        verbose_name_plural = "คำสั่งซื้อ"
        ordering = ['-created_at']


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="คำสั่งซื้อ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="สินค้า")
    quantity = models.IntegerField(verbose_name="จำนวน")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="ราคาต่อหน่วย")

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    class Meta:
        verbose_name = "รายการสินค้าในคำสั่งซื้อ"
        verbose_name_plural = "รายการสินค้าในคำสั่งซื้อ"

    def get_total(self):
        if self.quantity and self.price:
            return self.quantity * self.price
        return 0


class Notification(models.Model):
    TYPE_CHOICES = [
        ('order', 'คำสั่งซื้อ'),
        ('promotion', 'โปรโมชั่น'),
        ('system', 'ระบบ'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', verbose_name="ผู้ใช้")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="ประเภท")
    title = models.CharField(max_length=200, verbose_name="หัวข้อ")
    message = models.TextField(verbose_name="ข้อความ")
    link = models.CharField(max_length=200, blank=True, verbose_name="ลิงก์")
    is_read = models.BooleanField(default=False, verbose_name="อ่านแล้ว")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="วันที่สร้าง")

    def __str__(self):
        return f"{self.user.username} - {self.title}"

    class Meta:
        verbose_name = "การแจ้งเตือน"
        verbose_name_plural = "การแจ้งเตือน"
        ordering = ['-created_at']