from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):

    category_name = serializers.ReadOnlyField(
        source="category.name"
    )

    class Meta:

        model = Product

        fields = "__all__"
def validate_price(self, value):

    if value <= 0:
        raise serializers.ValidationError(
            "Price must be greater than zero."
        )

    return value


def validate_stock_quantity(self, value):

    if value < 0:
        raise serializers.ValidationError(
            "Stock cannot be negative."
        )

    return value