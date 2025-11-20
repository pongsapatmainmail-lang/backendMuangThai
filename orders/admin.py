from django.contrib import admin
from django.contrib import messages
from .models import Order, OrderItem, Notification

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price', 'item_total']
    can_delete = False

    def item_total(self, obj):
        if obj and obj.quantity and obj.price:
            return f"฿{(obj.quantity * obj.price):,.2f}"
        return "-"
    item_total.short_description = 'ยอดรวม'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total_price_display', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'shipping_name', 'shipping_phone']
    inlines = [OrderItemInline]
    readonly_fields = ['user', 'total_price', 'created_at', 'updated_at']
    
    fieldsets = (
        ('ข้อมูลคำสั่งซื้อ', {
            'fields': ('user', 'status', 'total_price', 'created_at', 'updated_at')
        }),
        ('ข้อมูลการจัดส่ง', {
            'fields': ('shipping_name', 'shipping_address', 'shipping_phone')
        }),
    )

    def total_price_display(self, obj):
        return f"฿{obj.total_price:,.2f}"
    total_price_display.short_description = 'ยอดรวม'

    def save_model(self, request, obj, form, change):
        if change:
            old_obj = Order.objects.get(pk=obj.pk)
            if old_obj.status != obj.status:
                # สร้างการแจ้งเตือนเมื่อเปลี่ยนสถานะ
                status_messages = {
                    'processing': 'กำลังเตรียมสินค้า',
                    'shipped': 'สินค้าถูกจัดส่งแล้ว',
                    'delivered': 'คุณได้รับสินค้าเรียบร้อยแล้ว',
                    'cancelled': 'คำสั่งซื้อถูกยกเลิก',
                }
                
                if obj.status in status_messages:
                    Notification.objects.create(
                        user=obj.user,
                        type='order',
                        title=f'อัพเดทสถานะคำสั่งซื้อ #{obj.id}',
                        message=status_messages[obj.status],
                        link=f'/orders'
                    )
                
                if old_obj.status != 'cancelled' and obj.status == 'cancelled':
                    messages.success(request, f'ยกเลิกคำสั่งซื้อ #{obj.id} สำเร็จ และคืนสต็อกสินค้าแล้ว')
        
        super().save_model(request, obj, form, change)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price', 'total_display']
    list_filter = ['order__status']
    
    def total_display(self, obj):
        if obj and obj.quantity and obj.price:
            return f"฿{(obj.quantity * obj.price):,.2f}"
        return "-"
    total_display.short_description = 'ยอดรวม'

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'type', 'title', 'is_read', 'created_at']
    list_filter = ['type', 'is_read', 'created_at']
    search_fields = ['user__username', 'title', 'message']
    readonly_fields = ['created_at']