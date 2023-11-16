from django.contrib.auth import views
from django.urls import path

urlpatterns = [
    path(
        "login",
        views.LoginView.as_view(template_name="customer/login.html"),
        name="login",
    ),
]
