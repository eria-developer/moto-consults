from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from . import models
from . import forms
from django.contrib import messages
from django.db.models import Sum
# Create your views here.

def dashboard(request):
    return HttpResponse(request, "Hi there")


def add_customer(request):
    if request.method == "POST":
        form = forms.CustomerForm(request.POST)
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

    context = {
        "form": form,
    }
    return render(request, "add_customer.html", context)


def edit_customer(request, customer_id):
    customer = get_object_or_404(models.Customer, id=customer_id)
    print(customer)
    if request.method == "POST":
        form = forms.EditCustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer details updated successfully")
            return redirect("view_customer", customer_id=customer.id)
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


# def view_customer(request, customer_id):
#     customer = get_object_or_404(models.Customer, id=customer_id)
#     customer_placements = models.RecruitmentProcess.objects.filter(customer=customer).order_by("-application_date")

#     customer_registration_fees = models.FeesPayment.objects.filter(customer=customer, fee_type="registration").first()
#     # print(f"PAid money: {customer_registration_fees.amount}")
#     default_registration_fee = models.RegistrationFees.objects.first() 
#     if customer_registration_fees:
#         customer_registration_fees = customer_registration_fees.amount
#         if default_registration_fee:
#             default_registration_fee = default_registration_fee.fees_amount
#             customer_registration_fees_balance = default_registration_fee - customer_registration_fees
#         else:
#             customer_registration_fees_balance = 0
#     else:
#         if default_registration_fee:
#             default_registration_fee = default_registration_fee.fees_amount
#         customer_registration_fees = 0
#         customer_registration_fees_balance = default_registration_fee

#     customer_connection_fees = models.FeesPayment.objects.filter(customer=customer, fee_type="connection").first()
#     if customer_connection_fees:
#         customer_connection_fees = customer_connection_fees.amount
#     else:
#         customer_registration_fees = 0

#     customer_consultation_fees = models.FeesPayment.objects.filter(customer=customer, fee_type="consultation")



#     context = {
#         "customer": customer,
#         "customer_placements": customer_placements,
#         "customer_registration_fees": customer_registration_fees,
#         "customer_connection_fees": customer_connection_fees,
#         "customer_consultation_fees": customer_consultation_fees,
#         "customer_registration_fees_balance": customer_registration_fees_balance,
        
#     }
#     print(context)
#     return render(request, "view_customer.html", context)


def view_customer(request, customer_id):
    customer = get_object_or_404(models.Customer, id=customer_id)
    customer_placements = models.RecruitmentProcess.objects.filter(customer=customer).order_by("-application_date")

    # Retrieving total paid registration fee for the customer
    total_registration_fees = models.FeesPayment.objects.filter(customer=customer, fee_type="registration") \
                                                  .aggregate(total_paid_registration=Sum('amount'))['total_paid_registration']
    customer_registration_fees = total_registration_fees if total_registration_fees else 0
    # Retrieving default registration fee
    default_registration_fee_obj = models.RegistrationFees.objects.first()
    default_registration_fee = default_registration_fee_obj.fees_amount if default_registration_fee_obj else 0
    # Calculating registration fee balance
    customer_registration_fees_balance = default_registration_fee - customer_registration_fees

    # Retrieving total paid connection fee for the customer
    total_connection_fees = models.FeesPayment.objects.filter(customer=customer, fee_type="connection") \
                                               .aggregate(total_paid_connection=Sum('amount'))['total_paid_connection']
    customer_connection_fees = total_connection_fees if total_connection_fees else 0
    # Retrieving default connection fee
    default_connection_fee_obj = models.ConnectionFees.objects.first()
    default_connection_fee = default_connection_fee_obj.fees_amount if default_connection_fee_obj else 0
    # Calculating connection fee balance
    customer_connection_fees_balance = default_connection_fee - customer_connection_fees

    # Handling consultation fees
    customer_consultation_fees = models.FeesPayment.objects.filter(customer=customer, fee_type="consultation")

    # Handling total amount paid and owed 
    total_amount_paid = customer_registration_fees + customer_connection_fees
    total_amount_owed = customer_registration_fees_balance + customer_connection_fees_balance

    context = {
        "customer": customer,
        "customer_placements": customer_placements,

        "customer_registration_fees": customer_registration_fees,
        "customer_registration_fees_balance": customer_registration_fees_balance,

        "customer_connection_fees": customer_connection_fees,
        "customer_connection_fees_balance": customer_connection_fees_balance,

        "customer_consultation_fees": customer_consultation_fees,

        "total_amount_paid": total_amount_paid,
        "total_amount_owed": total_amount_owed,
    }

    return render(request, "view_customer.html", context)


def delete_customer(request, customer_id):
    customer = get_object_or_404(models.Customer, id=customer_id)
    if request.method == "POST":
        customer.delete()
        return redirect("list-of-customers")
    

def list_of_customers(request):
    customers = models.Customer.objects.all()

    context = {
        "customers": customers,
    }
    return render(request, "list_of_customers.html", context)


def search_customer(request):
    pass