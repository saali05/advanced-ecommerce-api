"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path(
    "api/auth/",
    include("accounts.urls"),
    ),

    path(
    "api/",
    include("categories.urls"),
    ),

    path(
    "api/",
    include("products.urls"),
    ),
    path("api/cart/", include("cart.urls")),
    path(
    "api/orders/",
    include("orders.urls"),
    ),
    path(
    "api/dashboard/",
    include("dashboard.urls"),
    ),
    path(
    "api/admin/orders/",
    include("orders.admin_urls"),
    ),
    path(
    "api/admin/customers/",
    include("accounts.admin_urls"),
    ),
    path(
    "api/admin/products/",
    include("products.admin_urls"),
    ),


    path(
    "api/schema/",
    SpectacularAPIView.as_view(),
    name="schema",
    ),
    path(
    "swagger/",
    SpectacularSwaggerView.as_view(
    url_name="schema",
    ),
    name="swagger-ui",
    ),
    
]
