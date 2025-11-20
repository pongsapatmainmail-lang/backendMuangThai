from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # ฟิลด์ที่ใช้กรอง
    filterset_fields = ['category']
    
    # ฟิลด์ที่ใช้ค้นหา
    search_fields = ['name', 'description', 'category']
    
    # ฟิลด์ที่ใช้เรียงลำดับ
    ordering_fields = ['price', 'created_at', 'name']
    ordering = ['-created_at']  # เรียงตามวันที่สร้าง (ใหม่สุดก่อน)

    @action(detail=False, methods=['get'])
    def categories(self, request):
        """ดึงรายการหมวดหมู่ทั้งหมด"""
        categories = Product.objects.values_list('category', flat=True).distinct()
        # นับจำนวนสินค้าในแต่ละหมวด
        category_counts = []
        for cat in categories:
            count = Product.objects.filter(category=cat).count()
            category_counts.append({
                'name': cat,
                'count': count
            })
        return Response(category_counts)