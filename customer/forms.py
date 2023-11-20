from django import forms
from customer.models import Customer
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from customer.models import Customer
from django.utils.translation import gettext as _
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import password_validation

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


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



