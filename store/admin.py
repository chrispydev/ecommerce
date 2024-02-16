""" imports"""
from django.contrib import admin
from store.models import Product, Order, OrderItem, Cart, CartItem, Category, ShippingTax, ShippingRate, Size, MainCategory
# CartProductSize

class OrderItemInline(admin.TabularInline):
    model = OrderItem

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Filter the queryset to display only order items related to the current user
        if request.user.is_authenticated:
            queryset = queryset.filter(order__user=request.user)
        else:
            queryset = queryset.none()  # Return an empty queryset if the user is not authenticated
        return queryset

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'created_at')
    inlines = [OrderItemInline]

admin.site.register(Product)
admin.site.register(Category)
# admin.site.register(Order)
admin.site.register(OrderItem)
# admin.site.register(Order, OrderAdmin)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(ShippingTax)
admin.site.register(ShippingRate)
admin.site.register(Size)
admin.site.register(MainCategory)
# admin.site.register(CartProductSize)
