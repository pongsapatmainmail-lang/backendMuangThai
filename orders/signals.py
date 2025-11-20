from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Order

@receiver(pre_save, sender=Order)
def handle_order_cancellation(sender, instance, **kwargs):
    """คืนสต็อกเมื่อยกเลิก Order"""
    if instance.pk:  # ต้องเป็น order ที่มีอยู่แล้ว
        try:
            old_order = Order.objects.get(pk=instance.pk)
            
            # ถ้าเปลี่ยนจากสถานะอื่นเป็น cancelled
            if old_order.status != 'cancelled' and instance.status == 'cancelled':
                print(f"\n=== กำลังยกเลิกคำสั่งซื้อ #{instance.id} ===")
                
                # คืนสต็อกสินค้า
                for item in instance.items.all():
                    product = item.product
                    old_stock = product.stock
                    product.stock += item.quantity
                    product.save()
                    print(f"คืนสต็อก: {product.name}")
                    print(f"  จำนวน: +{item.quantity}")
                    print(f"  สต็อกเดิม: {old_stock} -> สต็อกใหม่: {product.stock}")
                
                print(f"=== คืนสต็อกเสร็จสิ้น ===\n")
                    
        except Order.DoesNotExist:
            pass