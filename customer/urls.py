from django.contrib.auth import views
from django.urls import path
from customer.views import RegisterForm

urlpatterns = [
    path('register', RegisterForm.as_view(), name='register'),
    path(
        "login",
        views.LoginView.as_view(template_name="customer/login.html"),
        name="login",
    ),
]
