from django import forms
from customer.models import Customer
from django.contrib.auth.models import User


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['address', 'phone_number', 'location']

class UserEmailUpdate(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['email']