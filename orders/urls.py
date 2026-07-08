from django.urls import path

from .views import (
    CheckoutAPIView,
    MyOrdersAPIView,
    OrderDetailAPIView,
    CancelOrderAPIView,
)

urlpatterns = [

    path(
        "checkout/",
        CheckoutAPIView.as_view(),
        name="checkout",
    ),

    path(
        "",
        MyOrdersAPIView.as_view(),
        name="my-orders",
    ),

    path(
        "<int:pk>/",
        OrderDetailAPIView.as_view(),
        name="order-detail",
    ),

    path(
        "<int:pk>/cancel/",
        CancelOrderAPIView.as_view(),
        name="cancel-order",
    ),
]