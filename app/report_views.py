from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from .models import FeesPayment, Expense, RegistrationFees, ConsultationFees, ConnectionFees, Customer
from django.db.models import Sum, F, Max, Min
from . import models
from decimal import Decimal

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
    start_date = None
    
    if time_frame == 'today':
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        report_title = f'Day: {current_date}'
    elif time_frame == 'week':
        start_of_week = now - timedelta(days=now.weekday())
        start_date = start_of_week
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
        hired_placements = models.RecruitmentProcess.objects.filter(status='hired', application_date__gte=start_date)
    else:
        payments = FeesPayment.objects.all()
        expenses = Expense.objects.all()
        hired_placements = models.RecruitmentProcess.objects.filter(status='hired')


    total_consultation_registration_fee = payments.filter(fee_type='consultation_registration').aggregate(total=Sum('amount'))['total'] or 0
    total_consultation_fee = payments.filter(fee_type='consultation').aggregate(total=Sum('amount'))['total'] or 0
    # total_connection_fee = payments.filter(fee_type='connection').aggregate(total=Sum('amount'))['total'] or 0
    # total_sales = total_consultation_registration_fee + total_consultation_fee + total_connection_fee

    # Calculate total connection fee owed
    connection_fee_percentage = ConnectionFees.objects.first().percentage if ConnectionFees.objects.exists() else Decimal('0')
    total_connection_fee_owed = Decimal('0')
    for placement in hired_placements:
        connection_fee = (Decimal(connection_fee_percentage) / Decimal('100')) * Decimal(placement.expected_salary)
        total_connection_fee_owed += connection_fee

    # Calculate total connection fee paid
    total_connection_fee_paid = payments.filter(fee_type='connection').aggregate(total=Sum('amount'))['total'] or Decimal('0')

    # Calculate outstanding connection fee
    outstanding_connection_fee = total_connection_fee_owed - total_connection_fee_paid

    total_sales = total_consultation_registration_fee + total_consultation_fee + total_connection_fee_paid



    total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0
    profit = total_sales - total_expenses

    consultation_registration_fee_default = RegistrationFees.objects.first().fees_amount
    consultation_fee_default = ConsultationFees.objects.first().fees_amount
    connection_fee_default = ConnectionFees.objects.first().percentage

    # outstanding_customers = []
    # total_outstanding_balance = 0
    # for customer in Customer.objects.all():
    #     consultation_registration_paid = customer.feespayment_set.filter(fee_type='consultation_registration').aggregate(total=Sum('amount'))['total'] or 0
    #     consultation_paid = customer.feespayment_set.filter(fee_type='consultation').aggregate(total=Sum('amount'))['total'] or 0
    #     connection_paid = customer.feespayment_set.filter(fee_type='connection').aggregate(total=Sum('amount'))['total'] or 0
        
    #     consultation_registration_owed = consultation_registration_fee_default - consultation_registration_paid
    #     consultation_owed = consultation_fee_default - consultation_paid
    #     connection_owed = connection_fee_default - connection_paid
    #     total_owed = consultation_registration_owed + connection_owed

    #     last_payment_date = customer.feespayment_set.aggregate(last_payment=Max('payment_date'))['last_payment']

    #     outstanding_customers.append({
    #         'customer': customer,
    #         'registration_owed': consultation_registration_owed,
    #         'consultation_owed': consultation_owed,
    #         'connection_owed': connection_owed,
    #         'total_owed': total_owed,
    #         'last_payment_date': last_payment_date,
    #     })

    #     total_outstanding_balance += total_owed

    outstanding_customers = []
    total_outstanding_balance = Decimal('0')
    for customer in Customer.objects.all():
        consultation_registration_paid = customer.feespayment_set.filter(fee_type='consultation_registration').aggregate(total=Sum('amount'))['total'] or Decimal('0')
        consultation_paid = customer.feespayment_set.filter(fee_type='consultation').aggregate(total=Sum('amount'))['total'] or Decimal('0')
        connection_paid = customer.feespayment_set.filter(fee_type='connection').aggregate(total=Sum('amount'))['total'] or Decimal('0')
        
        consultation_registration_owed = Decimal(consultation_registration_fee_default) - consultation_registration_paid
        consultation_owed = Decimal(consultation_fee_default) - consultation_paid
        
        # Calculate connection fee owed for this customer
        customer_hired_placements = hired_placements.filter(customer=customer)
        customer_connection_fee_owed = Decimal('0')
        for placement in customer_hired_placements:
            connection_fee = (Decimal(connection_fee_percentage) / Decimal('100')) * Decimal(placement.expected_salary)
            customer_connection_fee_owed += connection_fee
        
        connection_owed = customer_connection_fee_owed - connection_paid
        total_owed = consultation_registration_owed + connection_owed

        last_payment_date = customer.feespayment_set.aggregate(last_payment=Max('payment_date'))['last_payment']

        outstanding_customers.append({
            'customer': customer,
            'registration_paid': consultation_registration_paid,
            'registration_owed': consultation_registration_owed ,
            'connection_paid': connection_paid,
            'connection_owed': connection_owed,
            'total_owed': total_owed,
            'last_payment_date': last_payment_date,
        })

        total_outstanding_balance += total_owed

    # Highest and Lowest Payments
    highest_payment = payments.order_by('-amount').first()
    lowest_payment = payments.order_by('amount').first()
    
    highest_payment_amount = highest_payment.amount if highest_payment else 0
    highest_payment_customer = highest_payment.customer if highest_payment else "N/A"
    
    lowest_payment_amount = lowest_payment.amount if lowest_payment else 0
    lowest_payment_customer = lowest_payment.customer if lowest_payment else "N/A"

    # Highest and Lowest Expenses
    highest_expense = expenses.order_by('-amount').first()
    lowest_expense = expenses.order_by('amount').first()
    
    highest_expense_amount = highest_expense.amount if highest_expense else 0
    highest_expense_user = highest_expense.user if highest_expense else "N/A"
    
    lowest_expense_amount = lowest_expense.amount if lowest_expense else 0
    lowest_expense_user = lowest_expense.user if lowest_expense else "N/A"

    context = {
        'time_frame': time_frame,
        'total_registration_fee': total_consultation_registration_fee,
        'total_consultation_fee': total_consultation_fee,
        'total_connection_fee_owed': total_connection_fee_owed,
        'total_connection_fee_paid': total_connection_fee_paid,
        'outstanding_connection_fee': outstanding_connection_fee,
        'total_sales': total_sales,
        'total_expenses': total_expenses,
        'profit': profit,
        'payments': payments,
        'expenses': expenses,
        'outstanding_customers': outstanding_customers,
        "current_year": current_year,
        "current_month": current_month,
        "current_week": current_week,
        "current_date": current_date,
        "month_name": month_name,
        "report_title": report_title,
        "total_outstanding_balance": total_outstanding_balance,
        "highest_payment_amount": highest_payment_amount,
        "highest_payment_customer": highest_payment_customer,
        "lowest_payment_amount": lowest_payment_amount,
        "lowest_payment_customer": lowest_payment_customer,
        "highest_expense_amount": highest_expense_amount,
        "highest_expense_user": highest_expense_user,
        "lowest_expense_amount": lowest_expense_amount,
        "lowest_expense_user": lowest_expense_user,
    }

    if export_type == 'earnings':
        return generate_pdf('earnings_pdf_template.html', context)
    elif export_type == 'expenses':
        return generate_pdf('expenses_pdf_template.html', context)
    elif export_type == 'outstanding':
        return generate_pdf('outstanding_pdf_template.html', context)
    elif export_type == 'general':
        return generate_pdf('general_report.html', context)

    return render(request, 'reports.html', context)
