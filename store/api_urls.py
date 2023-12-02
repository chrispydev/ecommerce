from store.api_view import ProductListAPIView, ReportView
from django.urls import path

urlpatterns = [
    path("", ProductListAPIView.as_view()),
    path('add-products/', ReportView.as_view()),
]
