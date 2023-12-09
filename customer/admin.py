from django.contrib import admin

from customer.models import Customer, Message, AdminContact, Email, PhoneNumber

admin.site.register(Customer)
admin.site.register(Message)
admin.site.register(AdminContact)
admin.site.register(Email)
admin.site.register(PhoneNumber)
