from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100,null=True, help_text='Please this field is required')
    phone_number = PhoneNumberField(null=True, help_text='Please this field is required')
    region = models.CharField(max_length=20,null=True, help_text="Please this field is required")
    city = models.CharField(max_length=100,null=True, help_text="Please this field is required")
    nearest_location = models.CharField(max_length=100,null=True, help_text="Please this field is required")

    def __str__(self):
        return self.user.username


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    date_received = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.message

class AdminContact(models.Model):
    phone_number = PhoneNumberField(null=True)
    email = models.EmailField(max_length=255)

    def __str__(self):
        return f"{self.phone_number} && {self.email}"