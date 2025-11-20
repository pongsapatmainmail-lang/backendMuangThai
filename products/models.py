from django.db import models
from .shop_models import Shop

class Product(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='products', verbose_name="ร้านค้า", null=True)
    name = models.CharField(max_length=200, verbose_name="ชื่อสินค้า")
    description = models.TextField(verbose_name="รายละเอียด")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="ราคา")
    stock = models.IntegerField(default=0, verbose_name="จำนวนสินค้า")
    image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name="รูปภาพ")
    category = models.CharField(max_length=100, verbose_name="หมวดหมู่")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="วันที่สร้าง")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="วันที่แก้ไข")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "สินค้า"
        verbose_name_plural = "สินค้า"
        ordering = ['-created_at']