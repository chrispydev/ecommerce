from django.views.generic import ListView, DetailView
from store.models import Product, Order, OrderItem, Cart, CartItem, Category, ShippingTax, MainCategory
from django.views import View
from django.db.models import Sum,F
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from store.forms import CheckoutForm, UserEmailUpdate
import requests
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import os
from django.http import FileResponse, HttpResponse

class ProductListView(ListView):
    model = Product
    context_object_name = "products"
    template_name = "store/index.html"
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['main_categories'] = MainCategory.objects.all()
        return context


class ProductDetailView(DetailView):
    model = Product
    context_object_name = "product"
    template_name = "store/detail.html"

class CategoryProductListView(View):

    def get(self, request, name):
        category_name = name
        categories = Category.objects.all()
        main_categories = MainCategory.objects.all()
        queryset = Product.objects.all().order_by('name')
        if category_name:
            queryset = queryset.filter(category__name__iexact=category_name)

        paginator = Paginator(queryset, per_page=12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'category_products': page_obj,
            'categories': categories,
            'main_categories': main_categories,
            'product_total': len(queryset)
        }
        template_name = 'store/category_products.html'
        return render(request=request, template_name=template_name, context=context)

class SearchViewList(View):
    def get(self, request, search):
        api_url = f"http://localhost:8000/api/?search={search}"

        response = requests.get(api_url)

        data = response.json()

        categories = Category.objects.all()

        for product in data:
            product_image = product.get('product_image')
            if product_image:
                modified_product_image = product_image.replace("http://localhost:8000/https%3A/", "https://")
                product['product_image'] = modified_product_image

        context = {
            'category_products': data,
            'categories': categories,
            'page': 'product-search',
            'product_total': len(data)
        }
        return render(request, 'store/category_products.html', context)

class AddToCartView(View, LoginRequiredMixin):
    def post(self, request, *args, **kwargs):
        product_id = self.kwargs['product_id']
        product_size = self.kwargs['product_size']


        product = Product.objects.get(id=product_id)

        try:
            cart = Cart.objects.get(user=request.user)

            if product_size != 'None':
                print(product_size)
                cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, item_size=product_size)

                if created:
                    cart_item.quantity = 1
                else:
                    cart_item.quantity += 1

                cart_item.price = cart_item.quantity * product.price
                cart_item.save()
            else:
                cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
                if created:
                    cart_item.quantity = 1
                else:
                    cart_item.quantity += 1

                cart_item.price = cart_item.quantity * product.price
                cart_item.save()

        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=request.user)
            cart_item = CartItem.objects.create(
                cart=cart, product=product, quantity=1, price=product.price
            )

        # Calculate the total price
        total_price = cart.cartitem_set.aggregate(total_price=Sum("price"))[
            "total_price"
        ]

        # Calculate the total count of items in the cart
        cart_count = CartItem.objects.filter(cart=cart).aggregate(
            total_count=Sum("quantity")
        )["total_count"]

        # Return JSON response
        return JsonResponse({"cart_count": cart_count})


class CartItemsViewData(View, LoginRequiredMixin):
    def get(self, request):
        total_quantity = self.get_cart_items_for_current_user(request)

        return JsonResponse(
            { "total_quantity": total_quantity}
        )

    def get_cart_items_for_current_user(self, request):
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(cart__user=request.user)
            total_quantity = cart_items.aggregate(total_quantity=Sum("quantity"))[
                "total_quantity"
            ]
        else:
            cart_items = []
            total_quantity = 0

        return total_quantity

class CartListView(View, LoginRequiredMixin):
    def get(self, request):
        cart_items = self.get_cart_items_for_current_user(request)
        shippingTax = ShippingTax.objects.first()


        price_array = []

        for subtotal in cart_items:
            price_array.append(subtotal.quantity * subtotal.price)

        tax = shippingTax.tax * sum(price_array)
        total = sum(price_array) + tax
        decimal_places = 2
        round_ = round(total, decimal_places)
        tax_round = round(tax, decimal_places)

        context = {
            'cart_items': cart_items,
            'subtotal': sum(price_array),
            'tax': tax_round,
            'total': round_
        }

        template_name = 'store/cart_list.html'
        return render(request, template_name=template_name, context=context)

    def get_cart_items_for_current_user(self, request):
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(cart__user=request.user)
            total_quantity = cart_items.aggregate(total_quantity=Sum("quantity"))[
                "total_quantity"
            ]
        else:
            cart_items = []

        return cart_items



class OrderListView(ListView, LoginRequiredMixin):
    model = Order
    template_name = 'store/orders.html'
    context_object_name = 'orders'
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        queryset = queryset.prefetch_related('orderitem_set')  # Prefetch order items for efficiency
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        for order in context['orders']:
            order.total_quantity = order.orderitem_set.aggregate(total_quantity=Sum('quantity'))['total_quantity']
            order.total_price = order.orderitem_set.annotate(item_price=F('quantity') * F('price')).aggregate(total_price=Sum('item_price'))['total_price']

        return context

class OrderDetailView(DetailView):
    model = Order
    template_name = 'store/order_detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orderitems'] = self.object.orderitem_set.all()
        return context


class CartItemUpdateView(View, LoginRequiredMixin):
    def post(self, request, pk):
        cart_item = get_object_or_404(CartItem, id=pk)

        action = request.POST.get('action')

        if action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            elif cart_item.quantity == 1:
                cart_item.delete()
        elif action == 'increase':
            cart_item.quantity += 1
            cart_item.save()
        elif action == 'remove':
            cart_item.delete()

        return redirect('cart_list')


class CheckoutView(View):
    def get(self, request):
        cart_items = self.get_cart_items_for_current_user(request)

        c_form = CheckoutForm(instance=request.user.customer)
        u_form = UserEmailUpdate(instance=request.user)

        shippingTax = ShippingTax.objects.first()

        price_array = []

        for subtotal in cart_items:
            price_array.append(subtotal.quantity * subtotal.price)

        tax = shippingTax.tax * sum(price_array)
        total = sum(price_array) + tax
        decimal_places = 2
        round_ = round(total, decimal_places)
        tax_round = round(tax, decimal_places)

        context = {
            'subtotal': sum(price_array),
            'tax': tax_round,
            'total': round_,
            'c_form': c_form,
            'u_form': u_form,
            'cart_items': cart_items
        }

        template_name = 'store/checkout.html'
        return render(request, template_name, context)

    def get_cart_items_for_current_user(self, request):
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(cart__user=request.user)
            total_quantity = cart_items.aggregate(total_quantity=Sum("quantity"))[
                "total_quantity"
            ]
        else:
            cart_items = []

        return cart_items


class OrderConfirmView(DetailView):
    model = Order
    template_name = 'store/order_confirm.html'
    context_object_name = 'order_confirm'

    def get_object(self, queryset=None):
        # Get the last order for the current user
        user = self.request.user
        last_order = Order.objects.filter(user=user).order_by('-id').first()
        return last_order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve all the OrderItem objects associated with the last order
        order = self.get_object()
        order_items = order.orderitem_set.all()
        context['order_items'] = order_items
        # Add a success message
        messages.success(self.request, 'Thank you for ordering👍.')
        return context


class FileDownloadView(View):
    def get(self, request, *args, **kwargs):
        file_name = 'output.zip'  # Replace with the actual file name
        # vegetation, state regional

        # Get the directory of the current file
        current_directory = os.path.dirname(os.path.abspath(__file__))

        file_path = os.path.join(current_directory, file_name)

        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                # response = FileResponse(file)
                response = HttpResponse(file.read(), content_type="application/zip")
                # response['Content-Disposition'] = f'attachment; filename="{file_name}"'
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        else:
            return HttpResponse('File not found', status=404)
        return HttpResponse('<p>The is a text</p>')