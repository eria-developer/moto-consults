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

        widgets = {
            "firstname": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "othernames": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "phonenumber_1": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "phonenumber_2": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "address": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
            }),
            "passport_photo": forms.FileInput(attrs={
                "class": "form-control",
            }),
            "file_upload": forms.FileInput(attrs={
                "class": "form-control",
            }),
            "remarks": forms.Textarea(attrs={
                "class": "form-control",
            }),
        }


class CompanySearchForm(forms.Form):
    first_name = forms.CharField(required=False, label='First Name')
    last_name = forms.CharField(required=False, label='Last Name')
    email = forms.EmailField(required=False, label='Email')




# FORMS FOR COMPANY START 


class CompanyForm(forms.ModelForm):
    class Meta:
        model = models.EmployerCompany
        fields = "__all__"


class EditCompanyForm(forms.ModelForm):
    class Meta:
        model = models.EmployerCompany
        fields = "__all__"

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "phonenumber": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "address": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
            }),
        }


# class CompanySearchForm(forms.Form):
#     first_name = forms.CharField(required=False, label='First Name')
#     last_name = forms.CharField(required=False, label='Last Name')
#     email = forms.EmailField(required=False, label='Email')


# FORMS FOR COMPANY END 