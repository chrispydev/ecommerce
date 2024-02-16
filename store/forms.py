from django import forms
from django.forms import Select
from customer.models import Customer
from django.contrib.auth.models import User
from store.region_cites import REGION_CHOICES, CITES_IN_REGION


class CheckoutForm(forms.ModelForm):
    region = forms.ChoiceField(choices=REGION_CHOICES)
    city = forms.ChoiceField(choices=CITES_IN_REGION)
    class Meta:
        model = Customer
        fields = ['address', 'phone_number', 'region', 'city', 'nearest_location']
        widgets = {
            'region': Select(attrs={'class': 'form-control'}),
            'city': Select(attrs={'class': 'form-control'}),
        }

class UserEmailUpdate(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['email']