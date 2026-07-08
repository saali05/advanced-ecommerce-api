from django.urls import path

from .admin_views import CustomerListAPIView

urlpatterns = [

    path(
        "",
        CustomerListAPIView.as_view(),
    ),

]