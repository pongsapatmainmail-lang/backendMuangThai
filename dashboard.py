from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from datetime import timedelta
from orders.models import Order, OrderItem
from products.models import Product
from users.models import User

class DashboardAdminSite(admin.AdminSite):
    site_header = "Sunfun Shop Admin"
    site_title = "Sunfun Shop"
    index_title = "Dashboard"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name='dashboard'),
        ]
        return custom_urls + urls
    
    def dashboard_view(self, request):
        # คำนวณวันที่
        today = timezone.now().date()
        last_30_days = today - timedelta(days=30)
        last_7_days = today - timedelta(days=7)
        
        # สถิติรวม
        total_revenue = Order.objects.filter(
            status__in=['processing', 'shipped', 'delivered']
        ).aggregate(total=Sum('total_price'))['total'] or 0
        
        total_orders = Order.objects.count()
        total_products = Product.objects.count()
        total_users = User.objects.count()
        
        # สถิติ 30 วันล่าสุด
        revenue_30_days = Order.objects.filter(
            created_at__gte=last_30_days,
            status__in=['processing', 'shipped', 'delivered']
        ).aggregate(total=Sum('total_price'))['total'] or 0
        
        orders_30_days = Order.objects.filter(created_at__gte=last_30_days).count()
        
        # สถิติ 7 วันล่าสุด
        revenue_7_days = Order.objects.filter(
            created_at__gte=last_7_days,
            status__in=['processing', 'shipped', 'delivered']
        ).aggregate(total=Sum('total_price'))['total'] or 0
        
        orders_7_days = Order.objects.filter(created_at__gte=last_7_days).count()
        
        # คำสั่งซื้อล่าสุด 10 รายการ
        recent_orders = Order.objects.select_related('user').order_by('-created_at')[:10]
        
        # สินค้าขายดี Top 10
        top_products = OrderItem.objects.values(
            'product__name', 'product__id'
        ).annotate(
            total_sold=Sum('quantity'),
            total_revenue=Sum('quantity') * Sum('price')
        ).order_by('-total_sold')[:10]
        
        # สถิติตามสถานะ
        status_stats = Order.objects.values('status').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # ข้อมูลกราฟยอดขายรายวัน (7 วันล่าสุด)
        daily_revenue = []
        for i in range(7):
            date = today - timedelta(days=6-i)
            revenue = Order.objects.filter(
                created_at__date=date,
                status__in=['processing', 'shipped', 'delivered']
            ).aggregate(total=Sum('total_price'))['total'] or 0
            daily_revenue.append({
                'date': date.strftime('%d/%m'),
                'revenue': float(revenue)
            })
        
        context = {
            'total_revenue': total_revenue,
            'total_orders': total_orders,
            'total_products': total_products,
            'total_users': total_users,
            'revenue_30_days': revenue_30_days,
            'orders_30_days': orders_30_days,
            'revenue_7_days': revenue_7_days,
            'orders_7_days': orders_7_days,
            'recent_orders': recent_orders,
            'top_products': top_products,
            'status_stats': status_stats,
            'daily_revenue': daily_revenue,
        }
        
        return render(request, 'admin/dashboard.html', context)

# สร้าง instance
dashboard_admin_site = DashboardAdminSite(name='dashboard_admin')