from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from store.models import Product, Category, Order, OrderItem, Cart, CartItem
from customer.models import Customer, AdminContact
from store.serializers import ProductSerializer
from django.middleware.csrf import get_token
from django.http import JsonResponse
from faker import Faker
from django.db import transaction
from rest_framework.exceptions import ValidationError
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from store.text_message import send_text_message
from store.paystack_request import get_payment_method

class ProductListAPIView(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    filter_fields = ('id',)
    search_fields = ('name',)

class ReportView(APIView):
    """
    POST and GET method ONLY
    """

    def get(self, request):
        csrf_token = get_token(request)
        return JsonResponse({"csrftoken": csrf_token})

    def post(self, request):
        data = request.data
        self.validate(data)
        category = data.get('category')
        products = data.get('products')
        date = data.get('date')
        category_obj = self.get_category(category)
        response = self.handle_products(products, category_obj, date)
        return Response({"message": response})

    def handle_products(self, products, category_obj, date):
        fake = Faker()
        num_paragraphs = 4
        description = '\n\n'.join(fake.paragraph() for _ in range(num_paragraphs))

        response = []
        for product in products:
            obj, created = Product.objects.update_or_create(
                category=category_obj,
                    product_image= product.get('photo'),
                    description= description,
                    price=product.get('price'),
                    name= product.get('title'),)
            if created:
                response.append(f'{obj.product_image} - created')
                # response.append(f' - created')
            else:
                response.append(f'{obj.name} - updated')
        return response

    def get_category(self, category):
        obj, _ = Category.objects.get_or_create(name=category.title())
        return obj

    def validate(self, data):
        if data.get('category') is None:
            raise exceptions.ValidationError(
                'category is null'
            )
        if data.get('products') is None:
            raise exceptions.ValidationError(
                'products is null'
            )
        if data.get('date') is None:
            raise exceptions.ValidationError(
                'date is null'
            )


class OrderConfirmView(APIView):
    def post(self, request):
        user = request.user
        total = request.data.get('total')
        address = request.data.get('address')
        phone_number = request.data.get('phone_number')
        location = request.data.get('location')
        reference = request.data.get('transaction')

        try:
            payment_method = get_payment_method(reference)
            print(payment_method)
        except Exception as e:
            print(e)
        # return Response({"message": "Thank you"})

        with transaction.atomic():
            order = Order.objects.create(user=user, total=total, payment_method=payment_method)

            # Retrieve the user's cart
            try:
                cart = Cart.objects.get(user=user)
            except Cart.DoesNotExist:
                return Response({"message": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

            # Retrieve the cart items and create OrderItem objects for each item in the cart
            cart_items = CartItem.objects.filter(cart=cart)
            for cart_item in cart_items:
                OrderItem.objects.create(order=order, product=cart_item.product, price=cart_item.price,quantity=cart_item.quantity)

            # Delete the cart items
            cart_items.delete()

            # Delete the cart
            cart.delete()

            # Update the customer
            try:
                self.save_customer(user, address, phone_number, location)
                self.send_admin_message_text()
                send_text_message(phone_number,'Your order is being confirmed, Thank your for shopping with us')
            except Exception:
                return Response({"message": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

            # send gmail
            try:
                self.send_cemail(subject='Order Confirmation', message='Your order is being confirmed, Thank your for shopping with us', from_email='info@remgeeshop.com', to_email=user.email)
            except Exception as e:
                print(e)

        return Response({"message": "Thank you"})

    def save_customer(self, user, address, phone_number, location):
        customer = user.customer
        customer.address = address
        customer.phone_number = phone_number
        customer.location = location
        customer.save()

    def send_cemail(self, subject, message, from_email, to_email):
        subject = subject
        message = message
        from_email = from_email
        to_email = to_email
        send_mail(subject, message, from_email, [to_email])

    def send_admin_message_text(self):
        admin_contacts = AdminContact.objects.all()
        for admin_contact in admin_contacts:
            admin_subject = 'New Order Received'
            admin_message = f"A new order has been received."
            admin_from_email = 'info@remgeeshop.com'
            admin_to_email = admin_contact.email
            admin_to_contact = admin_contact.phone_number
            # send email to admin email
            send_mail(admin_subject, admin_message, admin_from_email, [admin_to_email])
            # Send text message to admin phone number
            send_text_message(str(admin_to_contact), 'New order received',)
