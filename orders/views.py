from decimal import Decimal
import uuid

from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Cart
from .models import (
    Order,
    OrderItem,
    OrderStatus,
    PaymentStatus,
)
from .serializers import OrderSerializer


class CheckoutAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        cart = get_object_or_404(
            Cart,
            customer=request.user,
        )

        if not cart.items.exists():

            return Response(
                {
                    "message": "Cart is empty."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        order = Order.objects.create(
            order_number="ORD-" + uuid.uuid4().hex[:8].upper(),
            customer=request.user,
            status=OrderStatus.PENDING,
            payment_status=PaymentStatus.UNPAID,
            shipping_address=request.user.profile.address,
        )

        total = Decimal("0.00")

        for item in cart.items.all():

            subtotal = item.product.price * item.quantity

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                unit_price=item.product.price,
                subtotal=subtotal,
            )

            total += subtotal

        order.total_amount = total
        order.save()

        cart.items.all().delete()

        serializer = OrderSerializer(order)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class MyOrdersAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        orders = Order.objects.filter(
            customer=request.user
        ).order_by("-created_at")

        serializer = OrderSerializer(
            orders,
            many=True,
        )

        return Response(serializer.data)


class OrderDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        order = get_object_or_404(
            Order,
            id=pk,
            customer=request.user,
        )

        serializer = OrderSerializer(order)

        return Response(serializer.data)


class CancelOrderAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        order = get_object_or_404(
            Order,
            id=pk,
            customer=request.user,
        )

        if order.status != OrderStatus.PENDING:

            return Response(
                {
                    "message": "Only pending orders can be cancelled."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Restore stock
        for item in order.items.all():

            product = item.product

            product.stock_quantity += item.quantity

            product.save()

        order.status = OrderStatus.CANCELLED

        order.save()

        return Response(
            {
                "message": "Order cancelled successfully."
            }
        )