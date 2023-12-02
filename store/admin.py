""" imports"""
from django.contrib import admin
from store.models import Product, Order, OrderItem, Cart, CartItem, Category

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'created_at')


admin.site.register(Product)
admin.site.register(Category)
# admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(CartItem)
