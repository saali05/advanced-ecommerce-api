from django.db import transaction
from rest_framework import serializers

from .models import User, CustomerProfile

from .models import User
class RegisterSerializer(serializers.Serializer):

    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    phone = serializers.CharField()

    address = serializers.CharField()
    city = serializers.CharField()
    state = serializers.CharField()
    country = serializers.CharField()
    postal_code = serializers.CharField()

    @transaction.atomic
    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            phone=validated_data["phone"],
        )

        user.role = "CUSTOMER"
        user.save()

        CustomerProfile.objects.create(
            user=user,
            address=validated_data["address"],
            city=validated_data["city"],
            state=validated_data["state"],
            country=validated_data["country"],
            postal_code=validated_data["postal_code"],
        )
        return user
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value


    def validate_phone(self, value):
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("Phone number already exists.")
        return value

    def to_representation(self, instance):

        return {
            "id": instance.id,
            "username": instance.username,
            "email": instance.email,
            "phone": instance.phone,
            "role": instance.role,
        }


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()

    password = serializers.CharField()


class CustomerProfileSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    phone = serializers.CharField(source="user.phone")

    class Meta:
        model = CustomerProfile
        fields = [
            "username",
            "email",
            "phone",
            "address",
            "city",
            "state",
            "country",
            "postal_code",
        ]

    def update(self, instance, validated_data):

        user_data = validated_data.pop("user", {})

        if "phone" in user_data:
            instance.user.phone = user_data["phone"]
            instance.user.save()

        return super().update(instance, validated_data)
    
def validate_email(self, value):

    if User.objects.filter(email=value).exists():
        raise serializers.ValidationError(
            "Email already exists."
        )

    return value

def validate_phone(self, value):

    if User.objects.filter(phone=value).exists():
        raise serializers.ValidationError(
            "Phone number already exists."
        )

    return value

def validate_username(self, value):

    if User.objects.filter(username=value).exists():
        raise serializers.ValidationError(
            "Username already exists."
        )

    return value