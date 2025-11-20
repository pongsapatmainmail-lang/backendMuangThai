from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .shop_views import ShopViewSet

router = DefaultRouter()
router.register(r'shops', ShopViewSet)

urlpatterns = [
    path('', include(router.urls)),
]