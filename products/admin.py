from django.contrib import admin
from .models import Product
from .shop_models import Shop

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'is_active', 'is_verified', 'created_at']
    list_filter = ['is_active', 'is_verified', 'created_at']
    search_fields = ['name', 'owner__username', 'email']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'shop', 'price', 'stock', 'category', 'created_at']
    list_filter = ['category', 'created_at', 'shop']
    search_fields = ['name', 'description', 'shop__name']