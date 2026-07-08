from django.urls import path

from .views import DashboardAPIView, dashboard

urlpatterns = [

    path(
        "",
        DashboardAPIView.as_view(),
    ),
        path(

        "dashboard/",

        dashboard,

        name="dashboard",

    ),

]