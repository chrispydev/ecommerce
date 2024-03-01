from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from store.models import Product, Category, Order, OrderItem, Cart, CartItem
from customer.models import Customer, AdminContact
from store.serializers import ProductSerializer, ShippingRateSerializer
from django.middleware.csrf import get_token
from django.http import JsonResponse
from faker import Faker
from django.db import transaction
from rest_framework.exceptions import ValidationError
from rest_framework import status
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from store.text_message import send_text_message
from store.paystack_request import get_payment_method
from store.models import ShippingRate
from django.contrib.auth.models import User
from django.template.loader import render_to_string

import os

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
        # user = User.objects.get(username=user)
        total = request.data.get('total')
        address = request.data.get('address')
        phone_number = request.data.get('phone_number')
        region = request.data.get('region')
        city = request.data.get('city')
        nearest_location = request.data.get('nearest_location')
        location = request.data.get('location')
        reference = request.data.get('transaction')

        try:
            payment_method = get_payment_method(reference)
        except Exception as e:
            print(e)

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
                OrderItem.objects.create(order=order, product=cart_item.product, price=cart_item.price,quantity=cart_item.quantity, size=cart_item.item_size)

            for cart_item in cart_items:
                product = Product.objects.get(name=cart_item.product.name)
                if (product.stock >= cart_item.quantity):
                    product.stock -= cart_item.quantity
                    product.save()
                    if product.stock == 0:
                        product.is_in_stock = False
                        product.save()
            self.handle_requests(address, phone_number, region, city, nearest_location,request, cart_items, cart, order)
        return Response({"message": "Thank you"})

    def handle_requests(self,address, phone_number, region, city, nearest_location, request, cart_items, cart, order):
        user = request.user
        # Delete the cart items
        cart_items.delete()

        # Delete the cart
        cart.delete()
        OrderItem = order.orderitem_set.all()

        # Update the customer
        try:
            self.save_customer(user, address, phone_number, region, city, nearest_location)
            self.send_admin_message_text(order, OrderItem)
            send_text_message(phone_number,'Your order is being confirmed, Thank your for shopping with us')
        except Exception as e:
            print(e)
            return Response({"message": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

        # send gmail
        try:
            # print('send sender message')
            self.send_cemail(subject='Order Confirmation', message='Your order is being confirmed, Thank your for shopping with us', from_email='info@remgeeshop.com', to_email=user.email)
        except Exception as e:
            print(e)


    def save_customer(self, user, address, phone_number, region, city, nearest_location):
        customer = Customer.objects.get(user=user)
        customer.user = user
        customer.address = address
        customer.phone_number = phone_number
        customer.region = region
        customer.city = city
        customer.nearest_location = nearest_location
        customer.save()

    def check_stock(self, product_name):
        product = Products.objects.get()

    def send_cemail(self, subject, message, from_email, to_email):
        subject = subject
        message = message
        from_email = from_email
        to_email = to_email
        send_mail(subject, message, from_email, [to_email])

    def send_admin_message_text(orderself, order, OrderItem):
        admin_contacts = AdminContact.objects.all()
        for admin_contact in admin_contacts:
            admin_subject = 'New Order Received'
            # admin_message = f"A new order has been received."
            admin_from_email = 'info@remgeeshop.com'
            admin_to_email = admin_contact.email
            admin_to_contact = admin_contact.phone_number

             # Render the HTML content using a template
            html_content = render_to_string('../templates/store/email_message.html', {'order_confirm': order, 'order_items': OrderItem})

            # send email to admin email
             # Create and send the email
            email = EmailMessage(admin_subject, body=html_content, from_email=admin_from_email, to=[admin_to_email])
            email.content_subtype = 'html'
            email.send()
            # Send text message to admin phone number
            send_text_message(str(admin_to_contact), 'New order received',)


class UpdateProductFileImage(APIView):
    def post(self, request):
        media_file = request.FILES.get('media_file')
        if media_file:
            file_name = os.path.splitext(media_file.name)[0]
            products = Product.objects.all()

            for product in products:
                image_file_name, image_file_extension = os.path.splitext(os.path.basename(product.product_image.name))
                product_file_name = image_file_name
                # print('-------------------')
                # print(f"file name:{file_name}")
                # print('-------------------')
                # print(f" product file name:{product_file_name}")

                if file_name.lower() in product_file_name.lower():
                    print("Product available:", product.product_image.url)
                    product.product_image = media_file
                    product.save()

            return Response({'message': 'File saved successfully.'})
        else:
            return Response({'message': 'No file provided.'}, status=400)

class CheckStock(APIView):
    def get(self, request):
        user = request.user
        with transaction.atomic():
            # Retrieve the user's cart
            try:
                cart = Cart.objects.get(user=user)
            except Cart.DoesNotExist:
                return Response({"message": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

            # Retrieve the cart items and create OrderItem objects for each item in the cart
            cart_items = CartItem.objects.filter(cart=cart)

            for cart_item in cart_items:
                product = Product.objects.get(name=cart_item.product.name)
                if (product.stock >= cart_item.quantity):
                    return Response({"message": f"{product.name} is in stock", "status": "200"}, status=status.HTTP_200_OK)
                elif (product.stock == 0):
                    print(f"{product.name} is out stock")
                    return Response({"message": f"{product.name} is out stock", "status": "403"}, status=status.HTTP_403_NOT_FOUND)
                elif (product.stock < cart_item.quantity and product.stock != 0):
                    print(f"{product.name} is less the quantity purchases so please reduce the quantity")
                    return Response({"message": f"{product.name} is less the quantity purchases so please reduce the quantity", "status": "404"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "this is the request"})

class ShippingRateListAPIView(ListAPIView):
    serializer_class = ShippingRateSerializer
    queryset = ShippingRate.objects.all()

    filter_fields = ('city',)
    search_fields = ('region',)