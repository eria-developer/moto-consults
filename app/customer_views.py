from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from . import models
from . import forms
from django.contrib import messages
from django.db.models import Sum, Q
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from decimal import Decimal


@login_required(login_url="/")
# Dashboard view
def dashboard(request):
    return HttpResponse("Hi there")


@login_required(login_url="/")
# View to add a new customer
def add_customer(request):
    if request.method == "POST":
        form = forms.CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer added successfully")
            return redirect("list-of-customers")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error} in {field}")
    else:
        form = forms.CustomerForm()

    context = {"form": form}
    return render(request, "add_customer.html", context)


@login_required(login_url="/")
# View to edit an existing customer
def edit_customer(request, customer_id):
    customer = get_object_or_404(models.Customer, id=customer_id)
    if request.method == "POST":
        form = forms.EditCustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer details updated successfully")
            return redirect("view-customer", customer_id=customer.id)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error} in {field}")
    else:
        form = forms.EditCustomerForm(instance=customer)

    context = {
        "form": form,
        "customer": customer,
    }
    return render(request, "edit_customer.html", context)


@login_required(login_url="/")
# View to display customer details
def view_customer(request, customer_id):
    customer = get_object_or_404(models.Customer, id=customer_id)
    customer_placements = models.RecruitmentProcess.objects.filter(customer=customer).order_by("-application_date")

    # Calculate total and default consultation_registration / consultation fees
    total_consultation_registration_fees = models.FeesPayment.objects.filter(customer=customer, fee_type="consultation_registration") \
                                                         .aggregate(total_paid_registration=Sum('amount'))['total_paid_registration'] or 0
    default_consultation_registration_fee = models.RegistrationFees.objects.first()
    default_consultation_registration_fee_amount = default_consultation_registration_fee.fees_amount if default_consultation_registration_fee else 0
    customer_consultation_registration_fees_balance = default_consultation_registration_fee_amount - total_consultation_registration_fees

     # Calculate connection fees based on hired placements
    hired_placements = customer_placements.filter(status='hired')
    total_connection_fees = Decimal('0.00')
    customer_connection_fees_balance = Decimal('0.00')
    for placement in hired_placements:
        connection_fee_percentage = models.ConnectionFees.objects.first().percentage if models.ConnectionFees.objects.exists() else Decimal('0')
        connection_fee = (Decimal(connection_fee_percentage) / Decimal('100')) * Decimal(placement.expected_salary)
        total_connection_fees += connection_fee

    # Calculate paid connection fees
    paid_connection_fees = models.FeesPayment.objects.filter(customer=customer, fee_type="connection") \
                                                     .aggregate(total_paid_connection=Sum('amount'))['total_paid_connection'] or Decimal('0')

    customer_connection_fees_balance = total_connection_fees - paid_connection_fees

    # Calculate total amount paid and owed
    total_amount_paid = Decimal(total_consultation_registration_fees) + paid_connection_fees
    total_amount_owed = Decimal(customer_consultation_registration_fees_balance) + customer_connection_fees_balance


    # Calculate total and default connection fees
    # total_connection_fees = models.FeesPayment.objects.filter(customer=customer, fee_type="connection") \
    #                                                   .aggregate(total_paid_connection=Sum('amount'))['total_paid_connection'] or 0
    # default_connection_fee = 0
    # default_connection_fee_amount = default_connection_fee.percentage if default_connection_fee else 0
    # customer_connection_fees_balance = default_connection_fee_amount - total_connection_fees

    # # Retrieve consultations and consultation fees
    # customer_consultations = models.Consultation.objects.filter(customer=customer).order_by("-consultation_date")
    # customer_consultation_fees_obj = models.FeesPayment.objects.filter(customer=customer, fee_type="consultation").order_by("-payment_date")

    # Calculate total amount paid and owed
    # total_amount_paid = total_consultation_registration_fees + paid_connection_fees
    # total_amount_owed = customer_consultation_registration_fees_balance + customer_connection_fees_balance

    context = {
         "customer": customer,
        "customer_placements": customer_placements,
        "customer_consultation_registration_fees": total_consultation_registration_fees,
        "customer_consultation_registration_fees_balance": customer_consultation_registration_fees_balance,
        "customer_connection_fees": paid_connection_fees,
        "customer_connection_fees_balance": customer_connection_fees_balance,
        "total_amount_paid": total_amount_paid,
        "total_amount_owed": total_amount_owed,
    }

    return render(request, "view_customer.html", context)


@login_required(login_url="/")
def delete_customer(request, customer_id):
    customer = get_object_or_404(models.Customer, id=customer_id)
    if request.method == "POST":
        customer.delete()
        messages.success(request, f"{customer.firstname} {customer.firstname} has been deleted successfully")
        return redirect("list-of-customers")


@login_required(login_url="/")
# View to list all customers
def list_of_customers(request):
    customers = models.Customer.objects.all().order_by("-date_added")

    context = {"customers": customers}
    return render(request, "list_of_customers.html", context)


@login_required(login_url="/")
# View to search for customers
def search_customers(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        query = request.GET.get("query", "")
        customers = models.Customer.objects.filter(
            Q(firstname__icontains=query) |
            Q(othernames__icontains=query) |
            Q(address__icontains=query) |
            Q(email__icontains=query) |
            Q(phonenumber_1__icontains=query) |
            Q(phonenumber_2__icontains=query)
        ).order_by("-date_added")

        customer_list = [
            {
                "id": customer.id,
                "firstname": customer.firstname,
                "othernames": customer.othernames,
                "phonenumber_1": customer.phonenumber_1,
                "phonenumber_2": customer.phonenumber_2,
                "email": customer.email,
                "address": customer.address,
                "date_added": customer.date_added.strftime("%Y-%m-%d %H:%M:%S"),
                "passport_photo": customer.passport_photo.url if customer.passport_photo else "",
                "file_upload": customer.file_upload.url if customer.file_upload else "",
                "remarks": customer.remarks,
                "view_url": reverse('view-customer', args=[customer.id]),
                "edit_url": reverse('edit-customer', args=[customer.id]),
                "delete_url": reverse('delete-customer', args=[customer.id]),
            }
            for customer in customers
        ]

        return JsonResponse({"customers": customer_list})
    return JsonResponse({"customers": []})
