from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "index.html")


def login_page(request):
    return render(request, "login.html")


def register_page(request):
    return render(request, "register.html")


def products(request):
    return render(request, "product.html")


def orders(request):
    return render(request, "orders.html")


def cart(request):
    return render(request, "cart.html")


def checkout(request):
    return render(request, "checkout.html")


def profile(request):
    return render(request, "profile.html")


def admin_dashboard(request):
    return render(request, "admin.html")