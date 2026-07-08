from django.urls import path
from . import views

urlpatterns = [

    path("", views.index, name="index"),

    path("login/", views.login_page, name="login"),

    path("register/", views.register_page, name="register"),

    path("products/", views.products, name="products"),

    path("orders/", views.orders, name="orders"),

    path("cart/", views.cart, name="cart"),

    path("checkout/", views.checkout, name="checkout"),

    path("profile/", views.profile, name="profile"),

    path("dashboard/", views.admin_dashboard, name="dashboard"),
]