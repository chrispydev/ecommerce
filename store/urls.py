from django.urls import path
from store.views import ProductListView, ProductDetailView, AddToCartView, CartItemsView, CheckOutView


urlpatterns = [
    path('', ProductListView.as_view(), name='product_home'),
    path('product-detail/<int:pk>/',
         ProductDetailView.as_view(), name='product_detail'),
    path('add-to-cart/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/count/', CartItemsView.as_view(), name='cart_count'),
    path('checkout/', CheckOutView.as_view(), name='checkout')
]
