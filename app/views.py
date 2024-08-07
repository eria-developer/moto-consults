from .customer_views import dashboard, add_customer, edit_customer, view_customer, delete_customer, list_of_customers, search_customers
from .company_views import add_company, edit_company, view_company, delete_company, list_of_companies, search_companies
from .job_views import add_job, edit_job, view_job, delete_job, list_of_jobs
from .jobposition_views import add_jobposition, edit_jobposition, view_jobposition, delete_jobposition, list_of_jobpositions
from .fee_views import add_fee, edit_fee, view_fee, delete_fee, list_of_fees, generate_receipt, preview_receipt
from .placement_views import add_placement, edit_placement, view_placement, delete_placement, list_of_placements, search_placements
from .consultation_views import add_consultation, view_consultation, list_of_consultations
from .expense_views import add_expense, list_of_expenses, list_of_expenses_of_all_users, edit_expense, delete_expense
from .settings_views import company_settings, roles, my_profile, edit_settings
from .report_views import reports

from django.shortcuts import render
from . import models
from . import forms
from authentication.models import CustomUser
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
import datetime
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from decimal import Decimal


@login_required(login_url="/")
def dashboard(request):
    total_customers = models.Customer.objects.count()
    total_companies = models.EmployerCompany.objects.count()
    total_jobs = models.Job.objects.count()
    total_placements = models.RecruitmentProcess.objects.count()

    now = timezone.now()
    start_of_week = now - timedelta(days=now.weekday())
    start_of_month = now.replace(day=1)
    start_of_year = now.replace(month=1, day=1)
    start_of_week_for_expenses = now - timedelta(days=now.weekday())
    start_of_month_for_expenses = now.replace(day=1)
    start_of_year_for_expenses = now.replace(month=1, day=1)

    total_week = models.FeesPayment.objects.filter(payment_date__gte=start_of_week).aggregate(Sum('amount'))['amount__sum'] or 0
    total_month = models.FeesPayment.objects.filter(payment_date__gte=start_of_month).aggregate(Sum('amount'))['amount__sum'] or 0
    total_year = models.FeesPayment.objects.filter(payment_date__gte=start_of_year).aggregate(Sum('amount'))['amount__sum'] or 0
    total_week_for_expenses = models.Expense.objects.filter(date_added__gte=start_of_week_for_expenses).aggregate(Sum('amount'))['amount__sum'] or 0
    total_month_for_expenses = models.Expense.objects.filter(date_added__gte=start_of_month_for_expenses).aggregate(Sum('amount'))['amount__sum'] or 0
    total_year_for_expenses = models.Expense.objects.filter(date_added__gte=start_of_year_for_expenses).aggregate(Sum('amount'))['amount__sum'] or 0

    total_custom_amount = None
    total_custom_amount_for_expenses = None

    start_date = None
    end_date = None
    start_date_for_expenses = None
    end_date_for_expenses = None

    custom_amount_form = forms.DateRangeForm()
    custom_amount_form_for_expenses = forms.DateRangeForm()

    recent_expenses = models.Expense.objects.order_by('-date_added')[:5]
    recent_fee_payments = models.FeesPayment.objects.order_by('-payment_date')[:5]

   # Retrieve the first connection fee object
    connection_fee = models.ConnectionFees.objects.first()
    # Check if the object exists and has a percentage attribute
    default_connection_fee = connection_fee.percentage if connection_fee is not None else 0

    # Retrieve the first consultation_registration fee object
    consultation_registration_fee = models.RegistrationFees.objects.first()
    # Check if the object exists and has a percentage attribute
    default_consultation_registration_fee = consultation_registration_fee.fees_amount if consultation_registration_fee is not None else 0

    # Get the time filter from the request (default to 'today')
    time_filter = request.GET.get('time_filter', 'today')
 
    # Initialize total amounts
    total_paid_consultation_registration = models.FeesPayment.objects.filter(
    fee_type='consultation_registration', 
    payment_status__in=['paid', 'partially_paid']
).aggregate(Sum('amount'))['amount__sum'] or 0

    total_customers = models.Customer.objects.count()
    total_expected_consultation_registration = total_customers * default_consultation_registration_fee
    total_unpaid_consultation_registration = total_expected_consultation_registration - total_paid_consultation_registration

    # Calculate totals for connection fees
    hired_placements = models.RecruitmentProcess.objects.filter(status='hired')
    
    total_expected_connection = Decimal('0')
    total_paid_connection = Decimal('0')
    total_unpaid_connection = Decimal('0')

    for placement in hired_placements:
        expected_fee = Decimal(placement.expected_salary) * (Decimal(default_connection_fee) / Decimal('100'))
        total_expected_connection += expected_fee

        paid_amount = models.FeesPayment.objects.filter(
            customer=placement.customer,
            fee_type='connection',
            payment_status__in=['paid', 'partially_paid']
        ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0')

        total_paid_connection += paid_amount
        total_unpaid_connection += expected_fee - paid_amount

    # total_paid_connection = 0
    # total_paid_consultation = 0

    # total_unpaid_consultation_registration = 0
    # total_unpaid_connection = 0
    # total_unpaid_consultation = 0

    # Retrieve all payments
    payments = models.FeesPayment.objects.all()

    # Retrieve payments within the time range
    payments_for_barchart = models.FeesPayment.objects.filter(payment_date__range=[start_date, end_date])

    # Data for the progress bar for customers 
    current_period_customers, increase_percentage_for_customers = models.Customer.calculate_progress()
    trend_for_customers = "Increase" if increase_percentage_for_customers >= 0 else "Decrease"

     # Data for the progress bar for companies 
    current_period_companies, increase_percentage_for_companies = models.EmployerCompany.calculate_progress()
    trend_for_companies = "Increase" if increase_percentage_for_companies >= 0 else "Decrease"

     # Data for the progress bar for jobs 
    current_period_jobs, increase_percentage_for_jobs = models.Job.calculate_progress()
    trend_for_jobs = "Increase" if increase_percentage_for_jobs >= 0 else "Decrease"

     # Data for the progress bar for placements 
    current_period_placements, increase_percentage_for_placements = models.RecruitmentProcess.calculate_progress()
    trend_for_placements = "Increase" if increase_percentage_for_placements >= 0 else "Decrease"



    # Calculate total paid and unpaid amounts for each fee type
    for payment in payments:
        if payment.fee_type == 'consultation_registration':
            if payment.payment_status == 'paid':
                total_paid_consultation_registration += payment.amount
            elif payment.payment_status == 'partially_paid':
                total_paid_consultation_registration += payment.amount
                total_unpaid_consultation_registration += default_consultation_registration_fee - payment.amount
            elif payment.payment_status == 'unpaid':
                total_unpaid_consultation_registration += default_consultation_registration_fee

        elif payment.fee_type == 'connection':
            if payment.payment_status == 'paid':
                total_paid_connection += payment.amount
            elif payment.payment_status == 'partially_paid':
                total_paid_connection += payment.amount
                total_unpaid_connection += default_connection_fee - payment.amount
            elif payment.payment_status == 'unpaid':
                total_unpaid_connection += default_connection_fee




    if request.method == 'POST':
        form_name = request.POST.get("form_name")

        if form_name == "custom_amount_date_form":
            custom_amount_form = forms.DateRangeForm(request.POST)
            if custom_amount_form.is_valid():
                start_date = custom_amount_form.cleaned_data['start_date']
                end_date = custom_amount_form.cleaned_data['end_date']

                total_custom_amount = models.FeesPayment.objects.filter(
                    payment_date__gte=start_date,
                    payment_date__lte=end_date
                ).aggregate(Sum('amount'))['amount__sum'] or 0

        elif form_name == "custom_amount_date_form_for_expenses":
            custom_amount_form_for_expenses = forms.DateRangeForm(request.POST)
            if custom_amount_form_for_expenses.is_valid():
                start_date_for_expenses = custom_amount_form_for_expenses.cleaned_data['start_date']
                end_date_for_expenses = custom_amount_form_for_expenses.cleaned_data['end_date']

                total_custom_amount_for_expenses = models.Expense.objects.filter(
                    date__gte=start_date_for_expenses,
                    date__lte=end_date_for_expenses
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
        "start_of_week_for_expenses": start_of_week_for_expenses,
        "start_of_month_for_expenses": start_of_month_for_expenses,
        "start_of_year_for_expenses": start_of_year_for_expenses,
        "total_week_for_expenses": total_week_for_expenses,
        "total_month_for_expenses": total_month_for_expenses,
        "total_year_for_expenses": total_year_for_expenses,
        "start_of_year_for_expenses": start_of_year_for_expenses,
        "total_custom_amount_for_expenses": total_custom_amount_for_expenses,
        "start_date_for_expenses": start_date_for_expenses,
        "end_date_for_expenses": end_date_for_expenses,
        "custom_amount_form_for_expenses": custom_amount_form_for_expenses,
        "recent_expenses": recent_expenses,
        "recent_fee_payments": recent_fee_payments,
        'total_paid_consultation_registration': total_paid_consultation_registration,
        'total_unpaid_consultation_registration': total_unpaid_consultation_registration,
        'total_paid_connection': total_paid_connection,
        'total_unpaid_connection': total_unpaid_connection,
        # 'total_paid_consultation': total_paid_consultation,
        # 'total_unpaid_consultation': total_unpaid_consultation,
        'time_filter': time_filter,
        "current_period_customers": current_period_customers,
        "increase_percentage_for_customers": increase_percentage_for_customers,
        "trend_for_customers": trend_for_customers,
        "current_period_companies": current_period_companies,
        "increase_percentage_for_companies": increase_percentage_for_companies,
        "trend_for_companies": trend_for_companies,
        "current_period_jobs": current_period_jobs,
        "increase_percentage_for_jobs": increase_percentage_for_jobs,
        "trend_for_jobs": trend_for_jobs,
        "current_period_placements": current_period_placements,
        "increase_percentage_for_placements": increase_percentage_for_placements,
        "trend_for_placements": trend_for_placements,
    }
    return render(request, "dashboard.html", context)


@login_required(login_url="/")
def aggregate_earnings(request, timeframe):
    now = timezone.now()
    
    if timeframe == 'day':
        start_date = now - timedelta(days=1)
    elif timeframe == 'week':
        start_date = now - timedelta(weeks=1)
    elif timeframe == 'month':
        start_date = now - timedelta(days=30)
    elif timeframe == 'year':
        start_date = now - timedelta(days=365)
    else:  # Custom dates
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
    
    payments = models.FeesPayment.objects.filter(payment_date__range=[start_date, now], payment_status='paid')
    
    data = {
        'consultation_registration': payments.filter(fee_type='consultation_registration').aggregate(Sum('amount'))['amount__sum'] or 0,
        # 'consultation': payments.filter(fee_type='consultation').aggregate(Sum('amount'))['amount__sum'] or 0,
        'connection': payments.filter(fee_type='connection').aggregate(Sum('amount'))['amount__sum'] or 0,
    }

    return JsonResponse(data)


def fetch_fee_payments(request):
    timeframe = request.GET.get('timeframe')
    now = timezone.now()

    if timeframe == 'day':
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = now.replace(hour=23, minute=59, second=59, microsecond=999999)
    elif timeframe == 'week':
        start_date = now - datetime.timedelta(days=now.weekday())
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + datetime.timedelta(days=6)
        end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
    elif timeframe == 'month':
        start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        next_month = now.replace(day=28) + datetime.timedelta(days=4)
        end_date = (next_month - datetime.timedelta(days=next_month.day)).replace(hour=23, minute=59, second=59, microsecond=999999)
    elif timeframe == 'year':
        start_date = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        end_date = now.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
    elif timeframe == 'custom':
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        start_date = timezone.make_aware(datetime.datetime.strptime(start_date, '%Y-%m-%d'))
        end_date = timezone.make_aware(datetime.datetime.strptime(end_date, '%Y-%m-%d'))
        # Set end_date to the end of the day
        end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
    else:
        return JsonResponse({'error': 'Invalid timeframe'})

    print(f"Timeframe: {timeframe}")
    print(f"Start Date: {start_date}")
    print(f"End Date: {end_date}")

    payments = models.FeesPayment.objects.filter(payment_date__range=[start_date, end_date])

    print(f"Payments: {payments}")

    data = {
        'consultation_registration': payments.filter(fee_type='consultation_registration').aggregate(Sum('amount'))['amount__sum'] or 0,
        # 'consultation': payments.filter(fee_type='consultation').aggregate(Sum('amount'))['amount__sum'] or 0,
        'connection': payments.filter(fee_type='connection').aggregate(Sum('amount'))['amount__sum'] or 0,
    }

    print(f"Data: {data}")

    return JsonResponse(data)
