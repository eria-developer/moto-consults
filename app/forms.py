from django import forms
from . import models


class CustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = "__all__"


class EditCustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = "__all__"


class CustomerSearchForm(forms.Form):
    first_name = forms.CharField(required=False, label='First Name')
    last_name = forms.CharField(required=False, label='Last Name')
    email = forms.EmailField(required=False, label='Email')