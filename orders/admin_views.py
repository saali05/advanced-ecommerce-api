from rest_framework import generics
from rest_framework.response import Response

from permissions import IsAdmin

from .models import Order
from .serializers import OrderSerializer


class AdminOrderListAPIView(generics.ListAPIView):

    queryset = Order.objects.all().order_by("-created_at")

    serializer_class = OrderSerializer

    permission_classes = [IsAdmin]


class AdminOrderDetailAPIView(generics.RetrieveAPIView):

    queryset = Order.objects.all()

    serializer_class = OrderSerializer

    permission_classes = [IsAdmin]


class AdminOrderUpdateAPIView(generics.UpdateAPIView):

    queryset = Order.objects.all()

    serializer_class = OrderSerializer

    permission_classes = [IsAdmin]

    http_method_names = [
        "patch",
    ]