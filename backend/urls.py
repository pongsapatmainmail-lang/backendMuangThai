from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # แยก path ของแต่ละ app ให้ชัดเจน
    path('api/products/', include('products.urls')),
    path('api/shop/', include('products.shop_urls')),
    path('api/users/', include('users.urls')),
    path('api/orders/', include('orders.urls')),
]

# สำหรับ media files ใน debug mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
