from django.contrib import admin
from .models import Product
from .shop_models import Shop
from django.utils.html import format_html

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

    actions = ['activate_shops', 'deactivate_shops']

    def activate_shops(self, request, queryset):
        queryset.update(is_active=True)
    activate_shops.short_description = "Activate selected shops"

    def deactivate_shops(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_shops.short_description = "Deactivate selected shops"


# ========== PRODUCT ADMIN ==========
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'shop', 'price', 'stock', 'category', 'image_preview', 'created_at']
    list_filter = ['category', 'shop', 'created_at']
    search_fields = ['name', 'description', 'shop__name', 'category__name']
    ordering = ['-created_at']

    readonly_fields = ['created_at', 'updated_at', 'image_preview']

    fieldsets = (
        ("ข้อมูลสินค้า", {
            "fields": ("name", "description", "category", "shop")
        }),
        ("ราคาและสต๊อก", {
            "fields": ("price", "stock")
        }),
        ("รูปภาพสินค้า", {
            "fields": ("image", "image_preview")
        }),
        ("วัน–เวลา", {
            "fields": ("created_at", "updated_at")
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 100px; height:auto;" />', obj.image.url)
        return "(ไม่มีรูป)"
    image_preview.short_description = "Preview"
