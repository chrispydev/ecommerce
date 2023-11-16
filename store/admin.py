""" imports"""
from django.contrib import admin
from store.models import Product, Order, OrderItem, Cart, CartItem


admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(CartItem)
