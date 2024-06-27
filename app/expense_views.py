from django.shortcuts import render, redirect
from . import forms, models
from django.contrib import messages


def add_expense(request):
    if request.method == "POST":
        form = forms.ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Expense added successfully!!")
            return redirect("list-of-expenses")
            print("Expense added successfully!!")
        else:
            for errors, field in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error} in {field}")
                    print(f"errors: {error} in {field}")
    form = forms.ExpenseForm()
    context = {
        "form": form
    }
    return render(request, "add_expense.html", context)


def list_of_expenses(request):
    expenses = models.Expense.objects.all().order_by("-date")
    add_expense_form = forms.ExpenseForm()

    if request.method == "POST":
        add_expense_form = forms.ExpenseForm(request.POST)
        if add_expense_form.is_valid():
            add_expense_form.save()
            messages.success(request, "Expense added successfully!!")
            return redirect("list-of-expenses")
            print("Expense added successfully!!")
        else:
            for errors, field in add_expense_form.errors.items():
                for error in errors:
                    messages.error(request, f"{error} in {field}")
                    print(f"errors: {error} in {field}")
    
    context = {
        "expenses": expenses,
        "add_expense_form": add_expense_form,
    }
    return render(request, "list_of_expenses.html", context)