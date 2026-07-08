from rest_framework.generics import ListAPIView

from permissions import IsAdmin

from .models import User
from .serializers import RegisterSerializer


class CustomerListAPIView(ListAPIView):

    serializer_class = RegisterSerializer

    permission_classes = [IsAdmin]

    def get_queryset(self):

        return User.objects.filter(
            role="CUSTOMER"
        )