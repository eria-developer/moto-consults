from .customer_views import dashboard, add_customer, edit_customer, view_customer, delete_customer, list_of_customers, search_customers
from .company_views import add_company, edit_company, view_company, delete_company, list_of_companies
from .job_views import add_job, edit_job, view_job, delete_job, list_of_jobs
from .jobposition_views import add_jobposition, edit_jobposition, view_jobposition, delete_jobposition, list_of_jobpositions
from .fee_views import add_fee, edit_fee, view_fee, delete_fee, list_of_fees, generate_receipt, preview_receipt
from .placement_views import add_placement, edit_placement, view_placement, delete_placement, list_of_placements, search_placements
from .consultation_views import add_consultation, view_consultation, list_of_consultations
from .expense_views import add_expense, list_of_expenses
from .settings_views import company_settings, roles, my_profile, edit_settings

from django.shortcuts import render
from . import models
from . import forms
from authentication.models import CustomUser
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta

def dashboard(request):
    total_customers = models.Customer.objects.count()
    total_companies = models.EmployerCompany.objects.count()
    total_jobs = models.Job.objects.count()
    total_placements = models.RecruitmentProcess.objects.count()

    now = timezone.now()
    start_of_week = now - timedelta(days=now.weekday())
    start_of_month = now.replace(day=1)
    start_of_year = now.replace(month=1, day=1)

    total_week = models.FeesPayment.objects.filter(payment_date__gte=start_of_week).aggregate(Sum('amount'))['amount__sum'] or 0
    total_month = models.FeesPayment.objects.filter(payment_date__gte=start_of_month).aggregate(Sum('amount'))['amount__sum'] or 0
    total_year = models.FeesPayment.objects.filter(payment_date__gte=start_of_year).aggregate(Sum('amount'))['amount__sum'] or 0
    total_custom_amount = None
    start_date = None
    end_date = None
    custom_amount_form = forms.DateRangeForm()

    if request.method == 'POST':
        custom_amount_form = forms.DateRangeForm(request.POST)
        form_name = request.POST.get("form_name")
        if form_name == "custom_amount_date_form":
            if custom_amount_form.is_valid():
                start_date = custom_amount_form.cleaned_data['start_date']
                end_date = custom_amount_form.cleaned_data['end_date']

                total_custom_amount = models.FeesPayment.objects.filter(
                    payment_date__gte=start_date,
                    payment_date__lte=end_date
                ).aggregate(Sum('amount'))['amount__sum'] or 0
    else:
        form = forms.DateRangeForm()


    context = {
        "total_customers": total_customers,
        "total_companies": total_companies,
        "total_jobs": total_jobs,
        "total_placements": total_placements,
        "total_week": total_week,
        "total_month": total_month,
        "total_year": total_year,
        "total_custom_amount": total_custom_amount,
        "start_date": start_date,
        "end_date": end_date,
        "custom_amount_form": custom_amount_form,
    }
    return render(request, "dashboard.html", context)