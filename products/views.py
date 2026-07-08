from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)

from rest_framework.viewsets import ModelViewSet

from .models import Product
from .serializers import ProductSerializer

from permissions import IsAdmin

class ProductViewSet(ModelViewSet):

    queryset = Product.objects.all()

    serializer_class = ProductSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "category",
        "is_active",
    ]

    search_fields = [
        "name",
        "sku",
        "description",
    ]

    ordering_fields = [
        "price",
        "stock_quantity",
        "created_at",
    ]

    def get_permissions(self):

        if self.action in [
            "list",
            "retrieve",
        ]:
            return []

        return [IsAdmin()]