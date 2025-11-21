from django.contrib import admin  # ← เพิ่มบรรทัดนี้
from django.urls import path, include
# from products.custom_admin import custom_admin_site  # ← comment ออก

urlpatterns = [
    path('admin/', admin.site.urls),  # ← เปลี่ยนเป็นบรรทัดนี้
    path('api/products/', include('products.urls')),
    path('api/shop/', include('products.shop_urls')),
    path('api/users/', include('users.urls')),
    path('api/orders/', include('orders.urls')),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)