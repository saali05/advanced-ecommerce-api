from rest_framework.generics import ListAPIView

from permissions import IsAdmin

from .models import Product
from .serializers import ProductSerializer


class LowStockAPIView(ListAPIView):

    serializer_class = ProductSerializer

    permission_classes = [IsAdmin]

    def get_queryset(self):

        return Product.objects.filter(
            stock_quantity__lte=5
        )