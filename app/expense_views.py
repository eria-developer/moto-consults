from django.shortcuts import render, redirect
from . import forms, models
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(login_url="/")
def add_expense(request):
    if request.method == "POST":
        form = forms.ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, "Expense added successfully!!")
            return redirect("list-of-expenses")
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


@login_required(login_url="/")
def list_of_expenses(request):
    expenses = models.Expense.objects.all().order_by("-date_added")
    my_expenses = models.Expense.objects.filter(user=request.user).order_by("-date_added")
    add_expense_form = forms.ExpenseForm()

    if request.method == "POST":
        add_expense_form = forms.ExpenseForm(request.POST)
        if add_expense_form.is_valid():
            add_expense_form.save()
            messages.success(request, "Expense added successfully!!")
            return redirect("list-of-expenses")
        else:
            for errors, field in add_expense_form.errors.items():
                for error in errors:
                    messages.error(request, f"{error} in {field}")
                    print(f"errors: {error} in {field}")
    
    context = {
        "expenses": expenses,
        "add_expense_form": add_expense_form,
        "my_expenses": my_expenses,
    }
    return render(request, "list_of_expenses.html", context)


@login_required(login_url="/")
def list_of_expenses_of_all_users(request):
    if request.user.role == "admin":
        expenses = models.Expense.objects.all().order_by("-date_added")
        add_expense_form = forms.ExpenseForm()

        if request.method == "POST":
            add_expense_form = forms.ExpenseForm(request.POST)
            if add_expense_form.is_valid():
                add_expense_form.save()
                messages.success(request, "Expense added successfully!!")
                return redirect("list-of-expenses")
            else:
                for errors, field in add_expense_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{error} in {field}")
                        print(f"errors: {error} in {field}")
    else:
        return redirect("list-of-expenses")
    
    context = {
        "expenses": expenses,
        "add_expense_form": add_expense_form,
    }
    return render(request, "list_of_expenses copy_for_all_users.html", context)