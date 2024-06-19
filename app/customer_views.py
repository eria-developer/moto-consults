from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from . import models
from . import forms
from django.contrib import messages
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

    context = {
        "customer": customer,
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