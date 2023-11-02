from django.views.generic import ListView, DetailView
from store.models import Product


class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'store/index.html'


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'store/detail.html'
