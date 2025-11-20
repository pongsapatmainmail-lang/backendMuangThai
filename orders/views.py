from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, Notification
from .serializers import OrderSerializer, CreateOrderSerializer, NotificationSerializer

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            order = serializer.save()
            order_serializer = OrderSerializer(order)
            return Response(order_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        
        if order.status != 'pending':
            return Response(
                {'error': 'ไม่สามารถยกเลิกคำสั่งซื้อนี้ได้'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # คืนสต็อกสินค้า
        for item in order.items.all():
            product = item.product
            product.stock += item.quantity
            product.save()
        
        order.status = 'cancelled'
        order.save()
        
        # สร้างการแจ้งเตือน
        Notification.objects.create(
            user=request.user,
            type='order',
            title='ยกเลิกคำสั่งซื้อแล้ว',
            message=f'คำสั่งซื้อ #{order.id} ถูกยกเลิกเรียบร้อยแล้ว',
            link=f'/orders'
        )
        
        serializer = self.get_serializer(order)
        return Response(serializer.data)


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        serializer = self.get_serializer(notification)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        self.get_queryset().update(is_read=True)
        return Response({'message': 'ทำเครื่องหมายอ่านทั้งหมดแล้ว'})

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        count = self.get_queryset().filter(is_read=False).count()
        return Response({'count': count})