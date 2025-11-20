from django.contrib import admin
from .models import Product
from .shop_models import Shop


# ========== SHOP ADMIN ==========
@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'is_active', 'is_verified', 'created_at']
    list_filter = ['is_active', 'is_verified', 'created_at']
    search_fields = ['name', 'owner__username', 'email']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    fieldsets = (
        ("ข้อมูลร้านค้า", {
            "fields": ("name", "description", "owner", "email")
        }),
        ("สถานะร้านค้า", {
            "fields": ("is_active", "is_verified"),
        }),
        ("วัน–เวลา", {
            "fields": ("created_at", "updated_at"),
        }),
    )


# ========== PRODUCT ADMIN ==========
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'shop', 'price', 'stock', 'category', 'created_at']
    list_filter = ['category', 'shop', 'created_at']
    search_fields = ['name', 'description', 'shop__name']
    ordering = ['-created_at']

    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ("ข้อมูลสินค้า", {
            "fields": ("name", "description", "category", "shop")
        }),
        ("ราคาและสต๊อก", {
            "fields": ("price", "stock")
        }),
        ("รูปภาพสินค้า", {
            "fields": ("image",)
        }),
        ("วัน–เวลา", {
            "fields": ("created_at", "updated_at")
        }),
    )
