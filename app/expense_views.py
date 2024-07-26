from django.shortcuts import render, redirect, get_object_or_404
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
# def list_of_expenses(request):
#     expenses = models.Expense.objects.all().order_by("-date_added")
#     my_expenses = models.Expense.objects.filter(user=request.user).order_by("-date_added")
#     add_expense_form = forms.ExpenseForm()

#     if request.method == "POST":
#         add_expense_form = forms.ExpenseForm(request.POST)
#         if add_expense_form.is_valid():
#             add_expense_form.save()
#             messages.success(request, "Expense added successfully!!")
#             return redirect("list-of-expenses")
#         else:
#             for errors, field in add_expense_form.errors.items():
#                 for error in errors:
#                     messages.error(request, f"{error} in {field}")
#                     print(f"errors: {error} in {field}")
    
#     context = {
#         "expenses": expenses,
#         "add_expense_form": add_expense_form,
#         "my_expenses": my_expenses,
#     }
#     return render(request, "list_of_expenses.html", context)
def list_of_expenses(request):
    my_expenses = models.Expense.objects.filter(user=request.user).order_by("-date_added")
    if 'edit_id' in request.GET:
        expense_id = request.GET['edit_id']
        expense = get_object_or_404(models.Expense, pk=expense_id)
        edit_expense_form = forms.EditExpenseForm(instance=expense)
    else:
        edit_expense_form = forms.EditExpenseForm()
        expenses = models.Expense.objects.all().order_by("-date_added")

    if request.method == 'POST':
        form_name = request.POST.get('form_name')
        if form_name == "edit_expense_form":
            expense_id = request.POST.get('expense_id')
            expense = get_object_or_404(models.Expense, pk=expense_id)
            edit_expense_form = forms.EditExpenseForm(request.POST, instance=expense)
            if edit_expense_form.is_valid():
                edit_expense_form.save()
                messages.success(request, "Expense updated successfully!")
                return redirect('list-of-expenses')
        elif form_name == "add_expense_form":
            add_expense_form = forms.ExpenseForm(request.POST)
            if add_expense_form.is_valid():
                add_expense_form.save()
                messages.success(request, "Expense added successfully!")
                return redirect('list-of-expenses')
    
    add_expense_form = forms.ExpenseForm()
    context = {
        "expenses": expenses,
        "edit_expense_form": edit_expense_form,
        "add_expense_form": add_expense_form,
        "my_expenses": my_expenses,
    }
    return render(request, "list_of_expenses.html", context)


@login_required(login_url="/")
def list_of_expenses_of_all_users(request):
    my_expenses = models.Expense.objects.filter(user=request.user).order_by("-date_added")
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
        "my_expenses": my_expenses,
    }
    return render(request, "list_of_expenses copy_for_all_users.html", context)



@login_required(login_url="/")
def edit_expense(request, expense_id):
    expense = get_object_or_404(models.Expense, id=expense_id)
    print(expense)
    if request.method == "POST":
        form = forms.EditExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, "Expense details updated successfully")
            return redirect("list-of-expenses")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error} in {field}")
    else:
        form = forms.EditExpenseForm(instance=expense)

    context = {
        "form": form,
        "expense": expense,
    }
    return render(request, "edit_expense.html", context)


@login_required(login_url="/")
def delete_expense(request, expense_id):
    expense = get_object_or_404(models.Expense, id=expense_id)
    if request.method == "POST":
        expense.delete()
        messages.success(request, f"{expense.name} has been deleted successfully")
        return redirect("list-of-expenses")