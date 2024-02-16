from store.api_view import ProductListAPIView, ReportView, OrderConfirmView, ShippingRateListAPIView, CheckStock, UpdateProductFileImage
from django.urls import path

urlpatterns = [
    path("", ProductListAPIView.as_view()),
    path('add-products/', ReportView.as_view()),
    path('order-confirm/', OrderConfirmView.as_view()),
    path('shipping-rate/', ShippingRateListAPIView.as_view()),
    path('update-productImage/', UpdateProductFileImage.as_view()),
    path('stock-check/', CheckStock.as_view()),
]
