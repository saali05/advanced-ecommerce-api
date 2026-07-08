from rest_framework import serializers

from .models import Cart, CartItem
from products.models import Product


class CartItemSerializer(serializers.ModelSerializer):

    product_name = serializers.ReadOnlyField(
        source="product.name"
    )

    price = serializers.ReadOnlyField(
        source="product.price"
    )

    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "product_name",
            "price",
            "quantity",
            "subtotal",
        ]

    def get_subtotal(self, obj):
        return obj.product.price * obj.quantity


class CartSerializer(serializers.ModelSerializer):

    items = CartItemSerializer(
        many=True,
        read_only=True,
    )

    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            "id",
            "items",
            "total",
        ]

    def get_total(self, obj):

        total = 0

        for item in obj.items.all():
            total += item.product.price * item.quantity

        return total


class AddCartItemSerializer(serializers.Serializer):

    product_id = serializers.IntegerField()

    quantity = serializers.IntegerField(
        min_value=1
    )