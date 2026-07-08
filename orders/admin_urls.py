from django.urls import path

from .admin_views import (
    AdminOrderListAPIView,
    AdminOrderDetailAPIView,
    AdminOrderUpdateAPIView,
)

urlpatterns = [

    path(
        "",
        AdminOrderListAPIView.as_view(),
    ),

    path(
        "<int:pk>/",
        AdminOrderDetailAPIView.as_view(),
    ),

    path(
        "<int:pk>/update/",
        AdminOrderUpdateAPIView.as_view(),
    ),

]