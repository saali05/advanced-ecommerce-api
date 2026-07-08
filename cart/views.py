from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cart, CartItem
from .serializers import (
    CartSerializer,
    AddCartItemSerializer,
)

from products.models import Product


class CartAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        cart, created = Cart.objects.get_or_create(
            customer=request.user
        )

        serializer = CartSerializer(cart)

        return Response(serializer.data)


class AddToCartAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = AddCartItemSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        product = get_object_or_404(
            Product,
            id=serializer.validated_data["product_id"],
        )

        quantity = serializer.validated_data["quantity"]

        if product.stock_quantity < quantity:

            return Response(
                {
                    "error": "Insufficient stock."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart, created = Cart.objects.get_or_create(
            customer=request.user
        )

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
        )

        if created:
            item.quantity = quantity
        else:
            item.quantity += quantity

        item.save()

        # Reduce stock
        product.stock_quantity -= quantity
        product.save()

        return Response(
            {
                "message": "Product added to cart."
            },
            status=status.HTTP_201_CREATED,
        )


class UpdateCartItemAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        item = get_object_or_404(
            CartItem,
            id=pk,
            cart__customer=request.user,
        )

        new_quantity = int(request.data.get("quantity"))

        old_quantity = item.quantity

        difference = new_quantity - old_quantity

        if difference > 0:

            if item.product.stock_quantity < difference:

                return Response(
                    {
                        "error": "Insufficient stock."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            item.product.stock_quantity -= difference

        elif difference < 0:

            item.product.stock_quantity += abs(difference)

        item.product.save()

        item.quantity = new_quantity

        item.save()

        return Response(
            {
                "message": "Cart updated successfully."
            }
        )


class DeleteCartItemAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        item = get_object_or_404(
            CartItem,
            id=pk,
            cart__customer=request.user,
        )

        product = item.product

        # Restore stock
        product.stock_quantity += item.quantity

        product.save()

        item.delete()

        return Response(
            {
                "message": "Item removed from cart."
            }
        )


class ClearCartAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request):

        cart, created = Cart.objects.get_or_create(
            customer=request.user
        )

        for item in cart.items.all():

            product = item.product

            # Restore stock
            product.stock_quantity += item.quantity

            product.save()

        cart.items.all().delete()

        return Response(
            {
                "message": "Cart cleared successfully."
            }
        )