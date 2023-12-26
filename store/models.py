""" module imports"""
from django.db import models
from django.contrib.auth.models import User
import uuid

class Category(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=300)
    product_image = models.ImageField(upload_to='media_file', default='default.jpg')
    product_image = models.URLField(default='http://localhost:8000/https%3A/images-na.ssl-images-amazon.com/images/I/616Vuoutx2L._AC_SX679_.jpg')
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default='iphone', null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):
    #     try:
    #         current_product = Product.objects.get(id=self.id)
    #         if current_product.product_image != self.product_image and current_product.product_image.name != 'default.jpg':
    #             default_storage.delete(current_product.product_image.name)
    #     except Product.DoesNotExist:
    #         pass

    #     super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

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

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

    def subtotal(self):
        return self.price * self.quantity


class ShippingTax(models.Model):
    shipping = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=8, decimal_places=2, default=0)

class CityManager(models.Manager):
    def cities_by_region(self, region):
        return self.filter(region=region)

class ShippingRate(models.Model):
    REGION_CHOICES = [
        ('Ashanti Region', 'Ashanti Region'),
        ('Brong-Ahafo Region', 'Brong-Ahafo Region'),
        ('Central Region', 'Central Region'),
        ('Eastern Region', 'Eastern Region'),
        ('Greater Accra Region', 'Greater Accra Region'),
        ('Northern Region', 'Northern Region'),
        ('Upper East Region', 'Upper East Region'),
        ('Upper West Region', 'Upper West Region'),
        ('Volta Region', 'Volta Region'),
        ('Western Region', 'Western Region'),
        ('Western North Region', 'Western North Region'),
        ('Oti Region', 'Oti Region'),
        ('Savannah Region', 'Savannah Region'),
        ('North East Region', 'North East Region'),
        ('Bono Region', 'Bono Region'),
        ('Ahafo Region', 'Ahafo Region')
    ]
    region = models.CharField(max_length=100, choices=REGION_CHOICES)
    city = models.CharField(max_length=100, default='please add a ciy')
    nearest_location = models.CharField(max_length=20)
    shipping_cost = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.region} - {self.nearest_location}'