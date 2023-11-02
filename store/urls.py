from django.urls import path
from store.views import ProductListView, ProductDetailView


urlpatterns = [
    path('', ProductListView.as_view(), name='product_home'),
    path('product-detail/<int:pk>/',
         ProductDetailView.as_view(), name='product_detail'),
]
