from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, default='please add an address')
    phone_number = PhoneNumberField(null=True, default='please add a number')
    location = models.CharField(max_length=20, default="Adenta Madina")

    def __str__(self):
        return self.user.username


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    date_received = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.message
