from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .shop_models import Shop
from .models import Product
from .shop_serializers import ShopSerializer, CreateShopSerializer, ShopProductSerializer

class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.filter(is_active=True)
    serializer_class = ShopSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'products']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        if self.action == 'my_shop':
            return Shop.objects.filter(owner=self.request.user)
        return Shop.objects.filter(is_active=True)

    def create(self, request, *args, **kwargs):
        # ตรวจสอบว่ามีร้านค้าแล้วหรือไม่
        if Shop.objects.filter(owner=request.user).exists():
            return Response(
                {'error': 'คุณมีร้านค้าอยู่แล้ว'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = CreateShopSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            shop = serializer.save()
            response_serializer = ShopSerializer(shop)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def my_shop(self, request):
        """ดูร้านค้าของตัวเอง"""
        try:
            shop = Shop.objects.get(owner=request.user)
            serializer = self.get_serializer(shop)
            return Response(serializer.data)
        except Shop.DoesNotExist:
            return Response({'error': 'คุณยังไม่มีร้านค้า'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        """ดูสินค้าของร้านค้า"""
        shop = self.get_object()
        products = Product.objects.filter(shop=shop)
        serializer = ShopProductSerializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_product(self, request):
        """เพิ่มสินค้าในร้านของตัวเอง"""
        try:
            shop = Shop.objects.get(owner=request.user)
        except Shop.DoesNotExist:
            return Response(
                {'error': 'คุณต้องสร้างร้านค้าก่อน'},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = request.data.copy()
        data['shop'] = shop.id

        serializer = ShopProductSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            product = serializer.save(shop=shop)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    def update_product(self, request, pk=None):
        """แก้ไขสินค้า"""
        try:
            shop = Shop.objects.get(owner=request.user)
            product = Product.objects.get(pk=pk, shop=shop)
        except Shop.DoesNotExist:
            return Response({'error': 'ไม่พบร้านค้า'}, status=status.HTTP_404_NOT_FOUND)
        except Product.DoesNotExist:
            return Response({'error': 'ไม่พบสินค้า'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ShopProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_product(self, request, pk=None):
        """ลบสินค้า"""
        try:
            shop = Shop.objects.get(owner=request.user)
            product = Product.objects.get(pk=pk, shop=shop)
            product.delete()
            return Response({'message': 'ลบสินค้าสำเร็จ'}, status=status.HTTP_204_NO_CONTENT)
        except Shop.DoesNotExist:
            return Response({'error': 'ไม่พบร้านค้า'}, status=status.HTTP_404_NOT_FOUND)
        except Product.DoesNotExist:
            return Response({'error': 'ไม่พบสินค้า'}, status=status.HTTP_404_NOT_FOUND)