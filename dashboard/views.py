from django.db.models import Sum

from rest_framework.views import APIView
from rest_framework.response import Response

from permissions import IsAdmin

from accounts.models import User
from categories.models import Category
from products.models import Product
from orders.models import Order, OrderStatus


class DashboardAPIView(APIView):

    permission_classes = [IsAdmin]

    def get(self, request):

        revenue = (
            Order.objects.filter(
                status=OrderStatus.DELIVERED
            ).aggregate(
                Sum("total_amount")
            )["total_amount__sum"]
            or 0
        )

        return Response({

            "customers": User.objects.filter(
                role="CUSTOMER"
            ).count(),

            "admins": User.objects.filter(
                role="ADMIN"
            ).count(),

            "categories": Category.objects.count(),

            "products": Product.objects.count(),

            "orders": Order.objects.count(),

            "pending_orders":
            Order.objects.filter(
                status=OrderStatus.PENDING
            ).count(),

            "confirmed_orders":
            Order.objects.filter(
                status=OrderStatus.CONFIRMED
            ).count(),

            "processing_orders":
            Order.objects.filter(
                status=OrderStatus.PROCESSING
            ).count(),

            "packed_orders":
            Order.objects.filter(
                status=OrderStatus.PACKED
            ).count(),

            "shipped_orders":
            Order.objects.filter(
                status=OrderStatus.SHIPPED
            ).count(),

            "delivered_orders":
            Order.objects.filter(
                status=OrderStatus.DELIVERED
            ).count(),

            "cancelled_orders":
            Order.objects.filter(
                status=OrderStatus.CANCELLED
            ).count(),

            "revenue": revenue,

        })