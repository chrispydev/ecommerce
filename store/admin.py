""" imports"""
from django.contrib import admin
from store.models import Customer, Product, Order, OrderItem


admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
