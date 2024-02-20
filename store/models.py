""" module imports"""
from django.db import models
from django.contrib.auth.models import User
import uuid
from store.region_cites import REGION_CHOICES, CITES_IN_REGION
from PIL import Image
# from django.core.files.storage import default_storage
import requests
from ckeditor.fields import RichTextField


class Category(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class MainCategory(models.Model):
    name = models.CharField(max_length=250)
    sub_categories = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return self.name

class Size(models.Model):
    display_text = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.display_text

class Product(models.Model):
    name = models.CharField(max_length=300)
    product_image = models.ImageField(upload_to='media_file', default='default.jpg')
    # product_image = models.URLField(default='http://localhost:8000/https%3A/images-na.ssl-images-amazon.com/images/I/616Vuoutx2L._AC_SX679_.jpg')
    # description = models.TextField()
    size = models.ManyToManyField(Size, blank=True)
    description = RichTextField(config_name='default')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default='iphone', null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_in_stock = models.BooleanField(default=True)
    has_sizes = models.BooleanField(default=False)
    stock = models.PositiveIntegerField(default=1)
    featured = models.BooleanField(default=False)
    has_discount = models.BooleanField(default=False)
    discount = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save()

        # img = Image.open(self.product_image.path)
        img = Image.open(requests.get(self.product_image.url, stream=True).raw)


        if img.height > 800 or img.width > 800:
            output_size = (800, 800)
            img.thumbnail(output_size)
            img.save(self.product_image.path)


class OrderItem(models.Model):
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    size = models.CharField(max_length=15, null=True)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

    def subtotal(self):
        return self.price * self.quantity

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=100, default='mobile_money')
    order_status = models.CharField(max_length=100, default='pending')

    ORDER_STATUSES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('delivery', 'Delivery'),
        ('delivered', 'Delivered'),
    )

    order_status = models.CharField(max_length=100, choices=ORDER_STATUSES, default='pending')

    def save(self, *args, **kwargs):
        # Generate a new order_id if it is not already set
        if not self.order_id:
            self.order_id = uuid.uuid4()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart #{self.id} - {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    item_size = models.TextField(max_length=20,null=True)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

    def subtotal(self):
        return self.price * self.quantity


class ShippingTax(models.Model):
    tax = models.DecimalField(max_digits=8, decimal_places=2, default=0)

class CityManager(models.Manager):
    def cities_by_region(self, region):
        return self.filter(region=region)

class ShippingRate(models.Model):
    region = models.CharField(max_length=100, choices=REGION_CHOICES)
    city = models.CharField(max_length=100, choices=CITES_IN_REGION)
    nearest_location = models.CharField(max_length=20)
    shipping_cost = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.region} - {self.nearest_location}'