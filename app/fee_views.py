from django.shortcuts import render, redirect, get_object_or_404
from . import models
from . import forms
from django.contrib import messages



def add_fee(request):
    if request.method == "POST":
        form = forms.FeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Fee added successfully")
            return redirect("list-of-fees")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error} in {field}")
    else:
        form = forms.FeeForm()

    customers = models.Customer.objects.all()
    fee_types = models.FeesPayment.CUSTOMER_FEE_CHOICES
    payment_status_choices = models.FeesPayment.STATUS_CHOICES

    context = {
        "form": form,
        "customers": customers,
        "fee_types": fee_types,
        "payment_status_choices": payment_status_choices,
    }
    return render(request, "add_fee.html", context)


def edit_fee(request, fee_id):
    fee = get_object_or_404(models.FeesPayment, id=fee_id)
    print(fee)
    if request.method == "POST":
        form = forms.EditFeeForm(request.POST, instance=fee)
        if form.is_valid():
            form.save()
            messages.success(request, "Fee details updated successfully")
            return redirect("view_fee", fee_id=fee.id)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error} in {field}")
    else:
        form = forms.EditFeeForm(instance=fee)

    context = {
        "form": form,
        "fee": fee,
    }
    return render(request, "edit_fee.html", context)


def view_fee(request, fee_id):
    fee = get_object_or_404(models.FeesPayment, id=fee_id)

    context = {
        "fee": fee,
    }
    return render(request, "view_fee.html", context)


def delete_fee(request, fee_id):
    fee = get_object_or_404(models.FeesPayment, id=fee_id)
    if request.method == "POST":
        fee.delete()
        return redirect("list-of-fees")
    

def list_of_fees(request):
    fees = models.FeesPayment.objects.all()

    context = {
        "fees": fees,
    }
    return render(request, "list_of_fees.html", context)
