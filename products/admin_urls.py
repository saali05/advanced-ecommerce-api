from django.urls import path

from .admin_views import LowStockAPIView

urlpatterns = [

    path(
        "low-stock/",
        LowStockAPIView.as_view(),
    ),

]