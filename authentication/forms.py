from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
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


class CustomUserUpdateForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('email', 'firstname', 'othernames', 'role', 'phone_number', 'pass_port_photo')

