from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import Order, OrderItem, Notification
from products.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_dashboard_stats(request):
    """สถิติภาพรวมสำหรับ Dashboard"""
    if not (request.user.is_staff or request.user.is_admin):
        return Response({'error': 'ไม่มีสิทธิ์เข้าถึง'}, status=status.HTTP_403_FORBIDDEN)
    
    # วันนี้
    today = timezone.now().date()
    
    # เดือนนี้
    month_start = today.replace(day=1)
    
    # สถิติคำสั่งซื้อ
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    processing_orders = Order.objects.filter(status='processing').count()
    completed_orders = Order.objects.filter(status='delivered').count()
    
    # รายได้
    total_revenue = Order.objects.filter(
        status__in=['delivered', 'shipped', 'processing']
    ).aggregate(total=Sum('total_price'))['total'] or 0
    
    monthly_revenue = Order.objects.filter(
        status__in=['delivered', 'shipped', 'processing'],
        created_at__gte=month_start
    ).aggregate(total=Sum('total_price'))['total'] or 0
    
    # สินค้า
    total_products = Product.objects.count()
    low_stock_products = Product.objects.filter(stock__lt=10).count()
    
    # ผู้ใช้
    total_users = User.objects.count()
    new_users_today = User.objects.filter(date_joined__date=today).count()
    
    return Response({
        'orders': {
            'total': total_orders,
            'pending': pending_orders,
            'processing': processing_orders,
            'completed': completed_orders
        },
        'revenue': {
            'total': float(total_revenue),
            'monthly': float(monthly_revenue)
        },
        'products': {
            'total': total_products,
            'low_stock': low_stock_products
        },
        'users': {
            'total': total_users,
            'new_today': new_users_today
        }
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_recent_orders(request):
    """คำสั่งซื้อล่าสุด"""
    if not (request.user.is_staff or request.user.is_admin):
        return Response({'error': 'ไม่มีสิทธิ์เข้าถึง'}, status=status.HTTP_403_FORBIDDEN)
    
    from .serializers import OrderSerializer
    orders = Order.objects.all()[:10]
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_low_stock_products(request):
    """สินค้าที่เหลือน้อย"""
    if not (request.user.is_staff or request.user.is_admin):
        return Response({'error': 'ไม่มีสิทธิ์เข้าถึง'}, status=status.HTTP_403_FORBIDDEN)
    
    from products.serializers import ProductSerializer
    products = Product.objects.filter(stock__lt=10).order_by('stock')
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def admin_update_order_status(request, pk):
    """อัพเดทสถานะคำสั่งซื้อ"""
    if not (request.user.is_staff or request.user.is_admin):
        return Response({'error': 'ไม่มีสิทธิ์เข้าถึง'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        order = Order.objects.get(pk=pk)
        new_status = request.data.get('status')
        
        if new_status:
            old_status = order.status
            order.status = new_status
            order.save()
            
            # สร้างการแจ้งเตือน
            status_messages = {
                'processing': 'กำลังเตรียมสินค้า',
                'shipped': 'สินค้าถูกจัดส่งแล้ว',
                'delivered': 'คุณได้รับสินค้าเรียบร้อยแล้ว',
                'cancelled': 'คำสั่งซื้อถูกยกเลิก',
            }
            
            if new_status in status_messages:
                Notification.objects.create(
                    user=order.user,
                    type='order',
                    title=f'อัพเดทสถานะคำสั่งซื้อ #{order.id}',
                    message=status_messages[new_status],
                    link=f'/orders'
                )
            
            from .serializers import OrderSerializer
            serializer = OrderSerializer(order)
            return Response(serializer.data)
    except Order.DoesNotExist:
        return Response({'error': 'ไม่พบคำสั่งซื้อ'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_send_notification(request):
    """ส่งการแจ้งเตือนถึงผู้ใช้"""
    if not (request.user.is_staff or request.user.is_admin):
        return Response({'error': 'ไม่มีสิทธิ์เข้าถึง'}, status=status.HTTP_403_FORBIDDEN)
    
    user_id = request.data.get('user_id')
    title = request.data.get('title')
    message = request.data.get('message')
    notification_type = request.data.get('type', 'system')
    link = request.data.get('link', '')
    
    if user_id == 'all':
        # ส่งถึงทุกคน
        users = User.objects.all()
        for user in users:
            Notification.objects.create(
                user=user,
                type=notification_type,
                title=title,
                message=message,
                link=link
            )
        return Response({'message': f'ส่งการแจ้งเตือนถึง {users.count()} คน'})
    else:
        # ส่งถึงคนเดียว
        try:
            user = User.objects.get(id=user_id)
            Notification.objects.create(
                user=user,
                type=notification_type,
                title=title,
                message=message,
                link=link
            )
            return Response({'message': 'ส่งการแจ้งเตือนสำเร็จ'})
        except User.DoesNotExist:
            return Response({'error': 'ไม่พบผู้ใช้'}, status=status.HTTP_404_NOT_FOUND)