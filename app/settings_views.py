from django.shortcuts import render, get_object_or_404
from .models import CompanySettings, Customer
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from . import models, forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(login_url="/")
def company_settings(request):

    # Initialize forms
    consultation_registration_form = forms.RegistrationForm()

    try:
        settings_instance = models.CompanySettings.objects.get()
        update_company_settings_form = forms.CompanySettingsForm(instance=settings_instance)
    except models.CompanySettings.DoesNotExist:
        settings_instance = None
        update_company_settings_form = forms.CompanySettingsForm()

    try:
        connection_fees_instance = models.ConnectionFees.objects.get()
        default_connection_fee = connection_fees_instance.percentage
    except models.ConnectionFees.DoesNotExist:
        connection_fees_instance = None
        default_connection_fee = 0

    try:
        consultation_registration_fees_instance = models.RegistrationFees.objects.get()
        default_consultation_registration_fee = consultation_registration_fees_instance.fees_amount
    except models.RegistrationFees.DoesNotExist:
        consultation_registration_fees_instance = None
        default_consultation_registration_fee = 0

    # try:
    #     consultation_fees_instance = models.ConsultationFees.objects.get()
    #     default_consultation_fee = consultation_fees_instance.fees_amount
    # except models.ConsultationFees.DoesNotExist:
    #     consultation_fees_instance = None
    #     default_consultation_fee = 0

    connection_fees_form = forms.ConnectionFeesForm(instance=connection_fees_instance)
    registration_fees_form = forms.RegistrationFeesForm(instance=consultation_registration_fees_instance)
    # consultation_fees_form = forms.ConsultationFeesForm(instance=consultation_fees_instance)

    if request.method == 'POST':
         # Handling form submissions based on the submitted form name
        form_name = request.POST.get('form_name')

        connection_fees_form = forms.ConnectionFeesForm(request.POST, instance=connection_fees_instance)
        registration_fees_form = forms.RegistrationFeesForm(request.POST, instance=consultation_registration_fees_instance)
        # consultation_fees_form = forms.ConsultationFeesForm(request.POST, instance=consultation_fees_instance)

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
                messages.success(request, 'Default registration / consultation fee successfully added!')
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


    context = {
        'settings_instance': settings_instance,
        "roles": roles,
        "consultation_registration_form": consultation_registration_form,
        "connection_fees_form": connection_fees_form,
        "consultation_registration_fees_form": registration_fees_form,
        # "consultation_fees_form": consultation_fees_form,
        "default_connection_fee": default_connection_fee,
        # "default_consultation_fee": default_consultation_fee,
        "default_consultation_registration_fee": default_consultation_registration_fee,
        "update_company_settings_form": update_company_settings_form,
    }
    return render(request, 'settings.html', context)



@login_required(login_url="/")
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
