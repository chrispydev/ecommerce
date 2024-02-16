from django.contrib import admin

from customer.models import Customer, Message,AdminContact

admin.site.register(Customer)
admin.site.register(Message)
admin.site.register(AdminContact)
