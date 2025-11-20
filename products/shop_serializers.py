from rest_framework import serializers
from .shop_models import Shop
from .models import Product
from django.contrib.auth import get_user_model

User = get_user_model()

class ShopSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    total_products = serializers.SerializerMethodField()
    total_sales = serializers.SerializerMethodField()

    class Meta:
        model = Shop
        fields = [
            'id', 'owner', 'owner_username', 'name', 'description', 
            'logo', 'banner', 'phone', 'email', 'address',
            'is_active', 'is_verified', 'created_at', 'updated_at',
            'total_products', 'total_sales'
        ]
        read_only_fields = ['owner', 'is_verified', 'created_at', 'updated_at']

    def get_total_products(self, obj):
        return obj.get_total_products()

    def get_total_sales(self, obj):
        return obj.get_total_sales()


class CreateShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['name', 'description', 'logo', 'banner', 'phone', 'email', 'address']

    def create(self, validated_data):
        user = self.context['request'].user
        shop = Shop.objects.create(owner=user, **validated_data)
        return shop


class ShopProductSerializer(serializers.ModelSerializer):
    shop_name = serializers.CharField(source='shop.name', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'shop', 'shop_name', 'name', 'description', 
            'price', 'stock', 'image', 'category', 'created_at'
        ]
        read_only_fields = ['shop']