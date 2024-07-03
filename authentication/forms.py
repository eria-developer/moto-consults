from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'firstname', 'othernames', 'role')

        widgets = {
            "email": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "firstname": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "othernames": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "role": forms.EmailInput(attrs={
                "class": "form-control",
            })
        }
