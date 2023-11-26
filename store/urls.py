from django.urls import path
from store.views import ProductListView, ProductDetailView, AddToCartView, CartItemsView, OrderListView, OrderDetailView


urlpatterns = [
    path('', ProductListView.as_view(), name='product_home'),
    path('product-detail/<int:pk>/',
         ProductDetailView.as_view(), name='product_detail'),
    path('add-to-cart/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/count/', CartItemsView.as_view(), name='cart_count'),
    path('account-order', OrderListView.as_view(), name='orders'),
    path('account-order-detail/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
]
