from django import forms
from . import models
# from authentication.models import 


class CustomerForm(forms.ModelForm):
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



# FORMS FOR COMPANY END 



# FORMS FOR JOB START 


class JobForm(forms.ModelForm):
    class Meta:
        model = models.Job
        fields = "__all__"

        widgets = {
            "job_title": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "job_position": forms.Select(attrs={
                "class": "form-control",
            }),
            "job_field": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "job_company": forms.Select(attrs={
                "class": "form-control",
            }),
            "job_description": forms.Textarea(attrs={
                "class": "form-control",
            }),
        }


class EditJobForm(forms.ModelForm):
    class Meta:
        model = models.Job
        fields = "__all__"

        widgets = {
            "job_title": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "job_position": forms.Select(attrs={
                "class": "form-control",
            }),
            "job_field": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "job_company": forms.Select(attrs={
                "class": "form-control",
            }),
            "job_description": forms.Textarea(attrs={
                "class": "form-control",
            }),
        }


# FORMS FOR JOB END 



# FORMS FOR JOB POSITIONS

class JobpositionForm(forms.ModelForm):
    class Meta:
        model = models.JobPosition
        fields = "__all__"

        widgets = {
            "job_position": forms.TextInput(attrs={
                "class": "form-control"
            })
        }


class EditJobpositionForm(forms.ModelForm):
    class Meta:
        model = models.JobPosition
        fields = "__all__"

        widgets = {
            "job_position": forms.TextInput(attrs={
                "class": "form-control",
            })
        }

# END FOR JOB POSITIONS FORMS 



# FORMS FOR FEES

class FeeForm(forms.ModelForm):
    class Meta:
        model = models.FeesPayment
        fields = "__all__"


class EditFeeForm(forms.ModelForm):
    class Meta:
        model = models.FeesPayment
        fields = "__all__"

        widgets = {
            "customer": forms.Select(attrs={
                "class": "form-control",
            }),
            "fee_type": forms.Select(attrs={
                "class": "form-control",
            }),
            "amount": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "payment_status": forms.Select(attrs={
                "class": "form-control",
            }),
        }

# END FOR FEES FORMS 



# FORMS FOR PLACEMENTS

class PlacementForm(forms.ModelForm):
    class Meta:
        model = models.RecruitmentProcess
        fields = "__all__"
        widgets = {
            "customer": forms.Select(attrs={
                "class": "form-control"
            }),
            "job": forms.Select(attrs={
                "class": "form-control",
            }),
            "status": forms.Select(attrs={
                "class": "form-control",
            }),
            "expected_salary": forms.NumberInput(attrs={
                "class": "form-control",
            }),
            "company": forms.Select(attrs={
                "class": "form-control"
            })
        }


class EditPlacementForm(forms.ModelForm):
    class Meta:
        model = models.RecruitmentProcess
        fields = "__all__"

        widgets = {
            "customer": forms.Select(attrs={
                "class": "form-control",
            }),
            "job": forms.Select(attrs={
                "class": "form-control",
            }),
            "status": forms.Select(attrs={
                "class": "form-control",
            }),
            "expected_salary": forms.NumberInput(attrs={
                "class": "form-control",
            }),
        }

# END FOR PLACEMMENTS FORMS 



# FORMS FOR CONSULTATIONS

class ConsultationForm(forms.ModelForm):
    class Meta:
        model = models.Consultation
        fields = "__all__"

        widgets = {
            "customer": forms.Select(attrs={
                "class": "form-control",
            }),
            "consultation_fee": forms.NumberInput(attrs={
                "class": "form-control",
            }),
        }


# END FOR CONSULTATION FORMS 


class CompanySettingsForm(forms.ModelForm):
    class Meta:
        model = models.CompanySettings
        fields = ['name', 'email', 'logo', 'favicon', 'address', 'phone_number']
        widgets = {
            'logo': forms.ClearableFileInput(attrs={'accept': 'image/*', 'class': 'form-control'}),
            'favicon': forms.ClearableFileInput(attrs={'accept': 'image/x-icon,image/vnd.microsoft.icon', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }


# class RoleForm(forms.ModelForm):
#     class Meta:
#         model = models.Role
#         fields = ['name', 'email', 'logo', 'favicon', 'address', 'phone_number']
#         widgets = {
#             'logo': forms.ClearableFileInput(attrs={'accept': 'image/*', 'class': 'form-control'}),
#             'favicon': forms.ClearableFileInput(attrs={'accept': 'image/x-icon,image/vnd.microsoft.icon', 'class': 'form-control'}),
#             'name': forms.TextInput(attrs={'class': 'form-control'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control'}),
#             'address': forms.Textarea(attrs={'class': 'form-control'}),
#             'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
#         }




# FORMS FOR REGISTRATION FEES

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = models.RegistrationFees
        fields = "__all__"

        widgets = {
            "fees_amount": forms.NumberInput(attrs={
                "class": "form-control",
            })
        }


# END FOR REGISTRATION FORMS 


# FORMS FOR REGISTRATION

class ConnectionFeesForm(forms.ModelForm):
    class Meta:
        model = models.ConnectionFees
        fields = "__all__"

        widgets = {
            "fees_amount": forms.NumberInput(attrs={
                "class": "form-control",
            })
        }


# END FOR REGISTRATION FORMS 


# FORMS FOR CONSULTATION

class ConsultationFeesForm(forms.ModelForm):
    class Meta:
        model = models.ConsultationFees
        fields = "__all__"

        widgets = {
            "fees_amount": forms.NumberInput(attrs={
                "class": "form-control",
            })
        }


# END FOR CONSULTATION FORMS 


# FORMS FOR REGISTRATION

class RegistrationFeesForm(forms.ModelForm):
    class Meta:
        model = models.RegistrationFees
        fields = "__all__"

        widgets = {
            "fees_amount": forms.NumberInput(attrs={
                "class": "form-control",
            })
        }


# END FOR REGISTRATION FORMS 