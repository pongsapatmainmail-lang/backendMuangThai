from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    shop_name = serializers.CharField(source='shop.name', read_only=True, allow_null=True)
    shop_id = serializers.IntegerField(source='shop.id', read_only=True, allow_null=True)

    class Meta:
        model = Product
        fields = [
            'id', 'shop', 'shop_id', 'shop_name', 'name', 'description', 
            'price', 'stock', 'image', 'category', 'created_at'
        ]