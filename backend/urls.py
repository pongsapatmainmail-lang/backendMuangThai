from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import Dashboard
from dashboard import dashboard_admin_site

# Import Models และ Admin Classes
from orders.admin import OrderAdmin, OrderItemAdmin, NotificationAdmin
from orders.models import Order, OrderItem, Notification
from products.models import Product
from users.models import User

# ตรวจสอบว่ามี ProductAdmin หรือไม่
try:
    from products.admin import ProductAdmin
    has_product_admin = True
except ImportError:
    has_product_admin = False
    
# ตรวจสอบว่ามี CategoryAdmin หรือไม่
try:
    from products.admin import CategoryAdmin
    from products.models import Category
    has_category_admin = True
except ImportError:
    has_category_admin = False

# ลงทะเบียน Models เข้า Custom Dashboard Admin
dashboard_admin_site.register(Order, OrderAdmin)
dashboard_admin_site.register(OrderItem, OrderItemAdmin)
dashboard_admin_site.register(Notification, NotificationAdmin)
dashboard_admin_site.register(User)  # ใช้ default admin

# ลงทะเบียน Product
if has_product_admin:
    dashboard_admin_site.register(Product, ProductAdmin)
else:
    dashboard_admin_site.register(Product)  # ใช้ default admin

# ลงทะเบียน Category (ถ้ามี)
if has_category_admin:
    dashboard_admin_site.register(Category, CategoryAdmin)

# URL Patterns
urlpatterns = [
    path('admin/', dashboard_admin_site.urls),  # ใช้ Custom Dashboard Admin
    path('api/products/', include('products.urls')),
    path('api/shop/', include('products.shop_urls')),
    path('api/users/', include('users.urls')),
    path('api/orders/', include('orders.urls')),
]

# Static และ Media Files สำหรับ Development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)