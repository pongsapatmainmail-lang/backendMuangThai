from rest_framework import serializers
from .models import Order, OrderItem, Notification
from products.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity', 'price', 'total']

    def get_total(self, obj):
        return obj.get_total()


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'user_username', 'status', 'total_price',
            'shipping_name', 'shipping_address', 'shipping_phone',
            'items', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'total_price', 'created_at', 'updated_at']


class CreateOrderSerializer(serializers.Serializer):
    shipping_name = serializers.CharField(max_length=100)
    shipping_address = serializers.CharField()
    shipping_phone = serializers.CharField(max_length=20)
    items = serializers.ListField(
        child=serializers.DictField()
    )

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("ต้องมีสินค้าอย่างน้อย 1 รายการ")
        return value

    def create(self, validated_data):
        from products.models import Product
        
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        
        # คำนวณยอดรวม
        total_price = 0
        order_items = []
        
        for item_data in items_data:
            product = Product.objects.get(id=item_data['product_id'])
            quantity = item_data['quantity']
            
            # ตรวจสอบสต็อก
            if product.stock < quantity:
                raise serializers.ValidationError(f"สินค้า {product.name} มีไม่เพียงพอ")
            
            total_price += product.price * quantity
            order_items.append({
                'product': product,
                'quantity': quantity,
                'price': product.price
            })
        
        # สร้าง Order
        order = Order.objects.create(
            user=user,
            total_price=total_price,
            **validated_data
        )
        
        # สร้าง OrderItems และอัพเดทสต็อก
        for item_data in order_items:
            OrderItem.objects.create(
                order=order,
                product=item_data['product'],
                quantity=item_data['quantity'],
                price=item_data['price']
            )
            
            # ลดสต็อกสินค้า
            product = item_data['product']
            product.stock -= item_data['quantity']
            product.save()
        
        # สร้างการแจ้งเตือน
        Notification.objects.create(
            user=user,
            type='order',
            title='สั่งซื้อสำเร็จ',
            message=f'คำสั่งซื้อ #{order.id} ของคุณได้รับการยืนยันแล้ว',
            link=f'/orders'
        )
        
        return order


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'type', 'title', 'message', 'link', 'is_read', 'created_at']
        read_only_fields = ['id', 'created_at']