from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from . import models
from . import forms
from django.contrib import messages
from django.db.models import Sum
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse

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

    # Handling consultations 
    customer_consultations = models.Consultation.objects.filter(customer=customer).order_by("-consultation_date")

    # Handling consultation fees
    customer_consultation_fees_obj = models.FeesPayment.objects.filter(customer=customer, fee_type="consultation").order_by("-payment_date")

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

        "customer_consultation_fees_obj": customer_consultation_fees_obj,

        "total_amount_paid": total_amount_paid,
        "total_amount_owed": total_amount_owed,

        "customer_consultations": customer_consultations,
    }

    return render(request, "view_customer.html", context)


def delete_customer(request, customer_id):
    customer = get_object_or_404(models.Customer, id=customer_id)
    if request.method == "POST":
        customer.delete()
        return redirect("list-of-customers")
    

def list_of_customers(request):
    customers = models.Customer.objects.all().order_by("-date")

    context = {
        "customers": customers,
    }
    return render(request, "list_of_customers.html", context)


def search_customer(request):
    # query = request.GET.get("query", "")
    # customers = models.Customer.objects.filter(
    #     Q(firstname__icontains = query) |
    #     Q(othernames__icontains = query) |
    #     Q(phonenumber_1__icontains = query) |
    #     Q(email__icontains = query) |
    #     Q(address__icontains = query) |
    #     Q(phonenumber_2__icontains = query) |
    # )
    pass


def search_customers(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        query = request.GET.get("query", "")
        customers = models.Customer.objects.filter(
            Q(firstname__icontains=query) |
            Q(othernames__icontains = query) |
            Q(address__icontains=query) |
            Q(email__icontains = query) |
            Q(phonenumber_1__icontains=query) |
            Q(phonenumber_2__icontains = query)
        ).order_by("-date")

        customer_list = []
        for customer in customers:
            customer_data = {
                "firstname": customer.firstname,
                "othernames": customer.othernames,
                "phonenumber_1": customer.phonenumber_1,
                "phonenumber_2": customer.phonenumber_2,
                "email": customer.email,
                "address": customer.address,
                "date": customer.date.strftime("%Y-%m-%d %H:%M:%S"),
                "passport_photo": customer.passport_photo.url if customer.passport_photo else "",
                "file_upload": customer.file_upload.url if customer.file_upload else "",
                "remarks": customer.remarks,
                "view_url": reverse('view-customer', args=[customer.id]),
                "edit_url": reverse('edit-customer', args=[customer.id]),
                "delete_url": reverse('delete-customer', args=[customer.id]),
            }
            customer_list.append(customer_data)

        return JsonResponse({"customers": customer_list})
    return JsonResponse({"customers": []})