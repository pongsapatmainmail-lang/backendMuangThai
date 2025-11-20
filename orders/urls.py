from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, NotificationViewSet
from .admin_views import (
    admin_dashboard_stats,
    admin_recent_orders,
    admin_low_stock_products,
    admin_update_order_status,
    admin_send_notification
)

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/stats/', admin_dashboard_stats, name='admin_stats'),
    path('admin/recent-orders/', admin_recent_orders, name='admin_recent_orders'),
    path('admin/low-stock/', admin_low_stock_products, name='admin_low_stock'),
    path('admin/orders/<int:pk>/status/', admin_update_order_status, name='admin_update_order_status'),
    path('admin/send-notification/', admin_send_notification, name='admin_send_notification'),
]