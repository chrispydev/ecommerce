from django.urls import path
from store.views import ProductListView, ProductDetailView, AddToCartView, CartItemsViewData, OrderListView, OrderDetailView,CategoryProductListView, SearchViewList, CartListView, CartItemUpdateView, CheckoutView, OrderConfirmView, FileDownloadView


urlpatterns = [
    path('', ProductListView.as_view(), name='product_home'),
    path('category-product/<str:name>/', CategoryProductListView.as_view(), name='category_product'),
    path('product-detail/<int:pk>/',
         ProductDetailView.as_view(), name='product_detail'),
    path('product-search/<str:search>/',
         SearchViewList.as_view(), name='product_search'),
    path('add-to-cart/<int:product_id>/<str:product_size>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart-list/', CartListView.as_view(), name='cart_list'),
    path('cart-update/<int:pk>/', CartItemUpdateView.as_view(), name='cart_update'),
    path('cart/count/', CartItemsViewData.as_view(), name='cart_count'),
    path('account-order', OrderListView.as_view(), name='orders'),
    path('account-order-detail/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('order-confirm/', OrderConfirmView.as_view(), name='order_confirm'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('download/', FileDownloadView.as_view(), name='download'),
]
