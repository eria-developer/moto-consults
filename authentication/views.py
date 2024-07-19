
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from . import models
from . import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.models import Expense
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy


@login_required(login_url="/")
def add_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully")
            return redirect('list-of-users')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error} in {field}")
                    print(f"Erros are: {error} in {field}")
    else:
        form = CustomUserCreationForm()

    role_choices = models.CustomUser.ROLE_CHOICES

    context = {
        'form': form,
        "role_choices": role_choices,
        }
    return render(request, 'add_user.html', context)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You have been logged out successfully.")
        return super().dispatch(request, *args, **kwargs)


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have been successfully logged in.')  # Add success message
                return redirect('dashboard')  # Redirect to appropriate page after login
            else:
                messages.error(request, 'Invalid username or password. Please try again.')  # Add error message
        else:
            messages.error(request, 'Invalid username or password. Please try again.')  # Add error message for form validation errors
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


@login_required(login_url="/")
def list_of_users(request):
    users = models.CustomUser.objects.all()
    role_choices = models.CustomUser.ROLE_CHOICES
    print(role_choices)

    context = {
        "users": users,
        "role_choices": role_choices,
    }
    return render(request, "list_of_users.html", context)


@login_required(login_url="/")
def delete_user(request, user_id):
    user = get_object_or_404(models.CustomUser, id=user_id)
    if request.method == "POST":
        user.delete()
        messages.success(request, f"{user.firstname} {user.firstname} has been deleted successfully")
        return redirect("list-of-users")


@login_required(login_url="/")
def view_user(request, user_id):
    user = get_object_or_404(models.CustomUser, id=user_id)
    expenses = Expense.objects.filter(user=user)

    context = {
        "user": user,
        "expenses": expenses,
    }
    return render(request, "view_user.html", context)


@login_required(login_url="/")
def edit_user(request, user_id):
    user = get_object_or_404(models.CustomUser, id=user_id)
    role_choices = models.CustomUser.ROLE_CHOICES

    if request.method == "POST":
        firstname = request.POST.get("firstname")
        othernames = request.POST.get("othernames")
        phone_number = request.POST.get("phone_number")
        email = request.POST.get("email")
        pass_port_photo = request.POST.get("pass_port_photo")
        role = request.POST.get("role")

        # Update the user object with new data
        user.firstname = firstname
        user.othernames = othernames
        user.phone_number = phone_number
        user.email = email
        user.pass_port_photo = pass_port_photo
        user.role = role

        # Save the updated user object
        user.save()

        messages.success(request, f"User '{user.firstname} {user.othernames}' updated successfully.")

        return redirect('view-user', user_id=user.id)


    context = {
        "user": user,
        "role_choices": role_choices,
    }
    return render(request, "view_user.html", context)