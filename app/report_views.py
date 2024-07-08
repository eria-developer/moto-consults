from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from .models import FeesPayment, Expense, RegistrationFees, ConsultationFees, ConnectionFees, Customer
from django.db.models import Sum, F, Max

def generate_pdf(template_src, context_dict):
    html_string = render_to_string(template_src, context_dict)
    html = HTML(string=html_string)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename={context_dict["time_frame"]}_report.pdf'
    html.write_pdf(response)
    return response

def get_week_of_month(date):
    first_day = date.replace(day=1)
    dom = date.day
    adjusted_dom = dom + first_day.weekday()
    return int((adjusted_dom - 1) / 7) + 1


def reports(request, time_frame, export_type=None):
    now = timezone.now()
    current_year = now.year
    current_date = now.strftime('%Y-%m-%d')
    current_month = now.strftime('%B %Y')
    current_week = get_week_of_month(now)
    month_name = now.strftime('%B')
    
    if time_frame == 'today':
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        report_title = f'Day: {current_date}'
    elif time_frame == 'week':
        start_date = now - timezone.timedelta(days=now.weekday())
        report_title = f'Week {current_week} of {month_name}'
    elif time_frame == 'month':
        start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        report_title = f'Month: {current_month}'
    elif time_frame == 'year':
        start_date = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        report_title = f'Year: {current_year}'
    else:
        start_date = None
        report_title = 'General Report'

    if start_date:
        payments = FeesPayment.objects.filter(payment_date__gte=start_date)
        expenses = Expense.objects.filter(date_added__gte=start_date)
    else:
        payments = FeesPayment.objects.all()
        expenses = Expense.objects.all()

    total_registration_fee = payments.filter(fee_type='registration').aggregate(total=Sum('amount'))['total'] or 0
    total_consultation_fee = payments.filter(fee_type='consultation').aggregate(total=Sum('amount'))['total'] or 0
    total_connection_fee = payments.filter(fee_type='connection').aggregate(total=Sum('amount'))['total'] or 0
    total_sales = total_registration_fee + total_consultation_fee + total_connection_fee

    total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0
    profit = total_sales - total_expenses

    # Get default fee amounts
    registration_fee_default = RegistrationFees.objects.first().fees_amount
    consultation_fee_default = ConsultationFees.objects.first().fees_amount
    connection_fee_default = ConnectionFees.objects.first().fees_amount

    # Calculate outstanding balances
    outstanding_customers = []
    for customer in Customer.objects.all():
        registration_paid = customer.feespayment_set.filter(fee_type='registration').aggregate(total=Sum('amount'))['total'] or 0
        consultation_paid = customer.feespayment_set.filter(fee_type='consultation').aggregate(total=Sum('amount'))['total'] or 0
        connection_paid = customer.feespayment_set.filter(fee_type='connection').aggregate(total=Sum('amount'))['total'] or 0
        
        registration_owed = registration_fee_default - registration_paid
        consultation_owed = consultation_fee_default - consultation_paid
        connection_owed = connection_fee_default - connection_paid
        total_owed = registration_owed + consultation_owed + connection_owed

        last_payment_date = customer.feespayment_set.aggregate(last_payment=Max('payment_date'))['last_payment']

        outstanding_customers.append({
            'customer': customer,
            'registration_owed': registration_owed,
            'consultation_owed': consultation_owed,
            'connection_owed': connection_owed,
            'total_owed': total_owed,
            'last_payment_date': last_payment_date,
        })

    context = {
        'time_frame': time_frame,
        'total_registration_fee': total_registration_fee,
        'total_consultation_fee': total_consultation_fee,
        'total_connection_fee': total_connection_fee,
        'total_sales': total_sales,
        'total_expenses': total_expenses,
        'profit': profit,
        'payments': payments,
        'expenses': expenses,
        'outstanding_customers': outstanding_customers,
        "current_year": current_year,
        "current_month": current_month,
        "current_week": current_week,
        "current_date,": current_date,
        "month_name": month_name,
        "report_title": report_title,
    }

    if export_type == 'earnings':
        return generate_pdf('earnings_pdf_template.html', context)
    elif export_type == 'expenses':
        return generate_pdf('expenses_pdf_template.html', context)
    elif export_type == 'outstanding':
        return generate_pdf('outstanding_pdf_template.html', context)

    return render(request, 'reports.html', context)
