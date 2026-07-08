from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets

from .models import Category
from .serializers import CategorySerializer
from .permissions import IsAdminOrReadOnly


class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all()

    serializer_class = CategorySerializer

    permission_classes = [IsAdminOrReadOnly]