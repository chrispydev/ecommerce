from django.contrib import admin

from customer.models import Customer, Message

admin.site.register(Customer)
admin.site.register(Message)
