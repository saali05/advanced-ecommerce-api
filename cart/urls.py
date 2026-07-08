from django.urls import path

from .views import (
    CartAPIView,
    AddToCartAPIView,
    UpdateCartItemAPIView,
    DeleteCartItemAPIView,
    ClearCartAPIView,
)

urlpatterns = [

    path(
        "",
        CartAPIView.as_view(),
    ),

    path(
        "add/",
        AddToCartAPIView.as_view(),
    ),

    path(
        "update/<int:pk>/",
        UpdateCartItemAPIView.as_view(),
    ),

    path(
        "delete/<int:pk>/",
        DeleteCartItemAPIView.as_view(),
    ),

    path(
        "clear/",
        ClearCartAPIView.as_view(),
    ),
]