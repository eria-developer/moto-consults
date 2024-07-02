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
import datetime
from django.http import JsonResponse

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
    total_week_for_expenses = models.Expense.objects.filter(date__gte=start_of_week_for_expenses).aggregate(Sum('amount'))['amount__sum'] or 0
    total_month_for_expenses = models.Expense.objects.filter(date__gte=start_of_month_for_expenses).aggregate(Sum('amount'))['amount__sum'] or 0
    total_year_for_expenses = models.Expense.objects.filter(date__gte=start_of_year_for_expenses).aggregate(Sum('amount'))['amount__sum'] or 0

    total_custom_amount = None
    total_custom_amount_for_expenses = None

    start_date = None
    end_date = None
    start_date_for_expenses = None
    end_date_for_expenses = None

    custom_amount_form = forms.DateRangeForm()
    custom_amount_form_for_expenses = forms.DateRangeForm()

    recent_expenses = models.Expense.objects.order_by('-date')[:5]
    recent_fee_payments = models.FeesPayment.objects.order_by('-payment_date')[:5]

    # Retrieve default fee amounts
    default_connection_fee = models.ConnectionFees.objects.first().fees_amount
    default_registration_fee = models.RegistrationFees.objects.first().fees_amount
    default_consultation_fee = models.ConsultationFees.objects.first().fees_amount

    # Get the time filter from the request (default to 'today')
    time_filter = request.GET.get('time_filter', 'today')
 
    # Initialize total amounts
    total_paid_registration = 0
    total_paid_connection = 0
    total_paid_consultation = 0

    total_unpaid_registration = 0
    total_unpaid_connection = 0
    total_unpaid_consultation = 0

    # Retrieve all payments
    payments = models.FeesPayment.objects.all()

    # Retrieve payments within the time range
    payments_for_barchart = models.FeesPayment.objects.filter(payment_date__range=[start_date, end_date])



    # Calculate total paid and unpaid amounts for each fee type
    for payment in payments:
        if payment.fee_type == 'registration':
            if payment.payment_status == 'paid':
                total_paid_registration += payment.amount
            elif payment.payment_status == 'partially_paid':
                total_paid_registration += payment.amount
                total_unpaid_registration += default_registration_fee - payment.amount
            elif payment.payment_status == 'unpaid':
                total_unpaid_registration += default_registration_fee

        elif payment.fee_type == 'connection':
            if payment.payment_status == 'paid':
                total_paid_connection += payment.amount
            elif payment.payment_status == 'partially_paid':
                total_paid_connection += payment.amount
                total_unpaid_connection += default_connection_fee - payment.amount
            elif payment.payment_status == 'unpaid':
                total_unpaid_connection += default_connection_fee

        elif payment.fee_type == 'consultation':
            if payment.payment_status == 'paid':
                total_paid_consultation += payment.amount
            elif payment.payment_status == 'partially_paid':
                total_paid_consultation += payment.amount
                total_unpaid_consultation += default_consultation_fee - payment.amount
            elif payment.payment_status == 'unpaid':
                total_unpaid_consultation += default_consultation_fee




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
        'total_paid_registration': total_paid_registration,
        'total_unpaid_registration': total_unpaid_registration,
        'total_paid_connection': total_paid_connection,
        'total_unpaid_connection': total_unpaid_connection,
        'total_paid_consultation': total_paid_consultation,
        'total_unpaid_consultation': total_unpaid_consultation,
        # 'start_date_for_barchart': start_date_for_barchart,
        # 'end_date_for_barchart': end_date_for_barchart,
        'time_filter': time_filter,
    }
    return render(request, "dashboard.html", context)


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
        'registration': payments.filter(fee_type='registration').aggregate(Sum('amount'))['amount__sum'] or 0,
        'consultation': payments.filter(fee_type='consultation').aggregate(Sum('amount'))['amount__sum'] or 0,
        'connection': payments.filter(fee_type='connection').aggregate(Sum('amount'))['amount__sum'] or 0,
    }

    return JsonResponse(data)



# from django.utils import timezone
# from django.http import JsonResponse
# from django.db.models import Sum
# import datetime
# from . import models

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
        start_date = timezone.make_aware(datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S'))
        end_date = timezone.make_aware(datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S'))
    else:
        return JsonResponse({'error': 'Invalid timeframe'})

    print(f"Timeframe: {timeframe}")
    print(f"Start Date: {start_date}")
    print(f"End Date: {end_date}")

    payments = models.FeesPayment.objects.filter(payment_date__range=[start_date, end_date])

    print(f"Payments: {payments}")

    data = {
        'registration': payments.filter(fee_type='registration').aggregate(Sum('amount'))['amount__sum'] or 0,
        'consultation': payments.filter(fee_type='consultation').aggregate(Sum('amount'))['amount__sum'] or 0,
        'connection': payments.filter(fee_type='connection').aggregate(Sum('amount'))['amount__sum'] or 0,
    }

    print(f"Data: {data}")

    return JsonResponse(data)
