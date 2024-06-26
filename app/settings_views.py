from django.shortcuts import render, get_object_or_404
from .models import CompanySettings, Customer
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from . import models, forms
from django.contrib import messages
from authentication.forms import RoleForm
from authentication.models import Roles


def company_settings(request):
    roles = Roles.objects.all()

    # Initialize forms
    role_form = RoleForm()
    registration_form = forms.RegistrationForm()

    try:
        settings_instance = models.CompanySettings.objects.get()
        update_company_settings_form = forms.CompanySettingsForm(instance=settings_instance)
    except models.CompanySettings.DoesNotExist:
        settings_instance = None
        update_company_settings_form = forms.CompanySettingsForm()

    try:
        connection_fees_instance = models.ConnectionFees.objects.get()
        default_connection_fee = connection_fees_instance.fees_amount
    except models.ConnectionFees.DoesNotExist:
        connection_fees_instance = None
        default_connection_fee = 0

    try:
        registration_fees_instance = models.RegistrationFees.objects.get()
        default_registration_fee = registration_fees_instance.fees_amount
    except models.RegistrationFees.DoesNotExist:
        registration_fees_instance = None
        default_registration_fee = 0

    try:
        consultation_fees_instance = models.ConsultationFees.objects.get()
        default_consultation_fee = consultation_fees_instance.fees_amount
    except models.ConsultationFees.DoesNotExist:
        consultation_fees_instance = None
        default_consultation_fee = 0

    connection_fees_form = forms.ConnectionFeesForm(instance=connection_fees_instance)
    registration_fees_form = forms.RegistrationFeesForm(instance=registration_fees_instance)
    consultation_fees_form = forms.ConsultationFeesForm(instance=consultation_fees_instance)

    if request.method == 'POST':
         # Handling form submissions based on the submitted form name
        form_name = request.POST.get('form_name')

        role_form = RoleForm(request.POST)
        connection_fees_form = forms.ConnectionFeesForm(request.POST, instance=connection_fees_instance)
        registration_fees_form = forms.RegistrationFeesForm(request.POST, instance=registration_fees_instance)
        consultation_fees_form = forms.ConsultationFeesForm(request.POST, instance=consultation_fees_instance)

        if form_name == 'update_company_settings_form':
            update_company_settings_form = forms.CompanySettingsForm(request.POST, request.FILES, instance=settings_instance)
            if update_company_settings_form.is_valid():
                update_company_settings_form.save()
                messages.success(request, 'Company settings successfully updated!')
                return redirect('company-settings')
            else:
                messages.error(request, 'An error occurred when saving the company settings.')

        if form_name == 'registration_fee_form':
            registration_fee_form = forms.RegistrationFeesForm(request.POST)
            if registration_fee_form.is_valid():
                registration_fee_form.save()
                messages.success(request, 'Default registration fee successfully added!')
                return redirect('company-settings')
            else:
                messages.error(request, 'An error occurred when saving the registration form.')

        elif form_name == 'connection_fee_form':
            connection_fee_form = forms.ConnectionFeesForm(request.POST)
            if connection_fee_form.is_valid():
                connection_fee_form.save()
                messages.success(request, 'Default connection fee successfully added!')
                return redirect('company-settings')
            else:
                messages.error(request, 'An error occurred when saving the connection form.')

        elif form_name == 'consultation_fee_form':
            consultation_fee_form = forms.ConsultationFeesForm(request.POST)
            if consultation_fee_form.is_valid():
                consultation_fee_form.save()
                messages.success(request, 'Default consultation fee successfully added!')
                return redirect('company-settings')
            else:
                messages.error(request, 'An error occurred when saving the consultation form.')

        elif form_name == 'role_form':
            role_form = RoleForm(request.POST)
            if role_form.is_valid():
                role_form.save()
                messages.success(request, 'User role successfully added!')
                return redirect('company-settings')
            else:
                messages.error(request, 'An error occurred when saving the user role.')

    context = {
        'settings_instance': settings_instance,
        "role_form": role_form,
        "roles": roles,
        "registration_form": registration_form,
        "connection_fees_form": connection_fees_form,
        "registration_fees_form": registration_fees_form,
        "consultation_fees_form": consultation_fees_form,
        "default_connection_fee": default_connection_fee,
        "default_consultation_fee": default_consultation_fee,
        "default_registration_fee": default_registration_fee,
        "update_company_settings_form": update_company_settings_form,
    }
    return render(request, 'settings.html', context)




@csrf_exempt 
def edit_settings(request):
    settings = CompanySettings.get_instance()
    form = models.CompanySettingsForm(instance=settings)
    if request.method == 'POST':
        form = forms.CompanySettingsForm(request.POST, request.FILES, instance=settings)
        if form.is_valid():
            form.save()
            return redirect('company_settings')
    return render(request, 'company_settings.html', {'form': form})



def roles(request):
    pass


def my_profile(request):
    pass


# def add_role(request):
#     if request.method == "POST":
#         form = forms.RoleForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Role added successfully")
#             return redirect("list-of-roles")
#         else:
#             for field, errors in form.errors.items():
#                 for error in errors:
#                     messages.error(request, f"{error} in {field}")
#                     print(f"{error} in {field}")
#     else:
#         form = forms.RoleForm()

#     context = {
#         "form": form,
#     }
#     return render(request, "add_role.html", context)


# def edit_role(request, role_id):
#     role = get_object_or_404(models.Roles, id=role_id)
#     print(role)
#     if request.method == "POST":
#         form = forms.EditRoleForm(request.POST, instance=role)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Role updated successfully")
#             return redirect("view_role", role_id=role.id)
#         else:
#             for field, errors in form.errors.items():
#                 for error in errors:
#                     messages.error(request, f"{error} in {field}")
#     else:
#         form = forms.EditRoleForm(instance=role)

#     context = {
#         "form": form,
#         "role": role,
#     }
#     return render(request, "edit_role.html", context)


# def delete_role(request, role_id):
#     role = get_object_or_404(models.Roles, id=role_id)
#     if request.method == "POST":
#         role.delete()
#         return redirect("list-of-roles")
    

# def list_of_roles(request):
#     roles = models.Role.objects.all()

#     context = {
#         "roles": roles,
#     }
#     return render(request, "list_of_roles.html", context)
