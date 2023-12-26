from django import forms
from django.forms import Select
from customer.models import Customer
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from customer.models import Customer
from django.utils.translation import gettext as _
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from store.region_cites import REGION_CHOICES, CITES_IN_REGION


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'password1': 'Password',
            'password2': 'Confirm Password',
        }


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.help_text = None  # Remove help text if desired

    def render_errors(self):
        error_messages = []
        for field_name, errors in self.errors.items():
            field_label = self.fields[field_name].label
            for error in errors:
                error_messages.append(f"{field_label}: {error}")
        return ", ".join(error_messages)





class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        existing_user = User.objects.exclude(pk=self.instance.pk).filter(email=email).exists()
        if existing_user:
            raise ValidationError("This email address is already in use.")
        return email


class CustomerUpdateForm(forms.ModelForm):
    region = forms.ChoiceField(choices=REGION_CHOICES)
    city = forms.ChoiceField(choices=CITES_IN_REGION)
    class Meta:
        model = Customer
        fields = ['address', 'phone_number', 'region', 'city', 'nearest_location']
        widgets = {
            'region': Select(attrs={'class': 'form-control'}),
            'city': Select(attrs={'class': 'form-control'}),
        }