from django.views.generic import ListView, DetailView
from store.models import Product, Order, OrderItem, Cart, CartItem
from django.views import View
from django.db.models import Sum
from django.shortcuts import redirect, render
from django.http import JsonResponse
# from customer.models import Customer


class ProductListView(ListView):
    model = Product
    context_object_name = "products"
    template_name = "store/index.html"


class ProductDetailView(DetailView):
    model = Product
    context_object_name = "product"
    template_name = "store/detail.html"


class AddToCartView(View):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get("product_id")
        product = Product.objects.get(id=product_id)

        try:
            cart = Cart.objects.get(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, product=product
            )

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


class CartItemsView(View):
    def get(self, request):
        cart_items, total_quantity = self.get_cart_items_for_current_user(request)
        serialized_cart_items = self.serialize_cart_items(cart_items)
        return JsonResponse(
            {"cart_items": serialized_cart_items, "total_quantity": total_quantity}
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

        return cart_items, total_quantity

    def serialize_cart_items(self, cart_items):
        serialized_items = []
        for cart_item in cart_items:
            serialized_items.append(
                {
                    "product": cart_item.product.name,
                    "quantity": cart_item.quantity,
                    "price": str(cart_item.price),
                    "subtotal": str(cart_item.subtotal()),
                }
            )

        return serialized_items


