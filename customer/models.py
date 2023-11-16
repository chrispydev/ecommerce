from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    phone_number = PhoneNumberField()
    location = models.CharField(max_length=20, default="Adenta Madina")

    def __str__(self):
        return self.user.username
