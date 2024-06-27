
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from . import models
from . import forms
from django.contrib import messages

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

    role_choices = models.Roles.objects.all()

    context = {
        'form': form,
        "role_choices": role_choices,
        }
    return render(request, 'add_user.html', context)

# def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request, username=email, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('list-of-customers')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'login.html', {'form': form})


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
                return redirect('list-of-customers')  # Redirect to appropriate page after login
            else:
                messages.error(request, 'Invalid username or password. Please try again.')  # Add error message
        else:
            messages.error(request, 'Invalid username or password. Please try again.')  # Add error message for form validation errors
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def list_of_users(request):
    users = models.CustomUser.objects.all()

    context = {
        "users": users,
    }
    return render(request, "list_of_users.html", context)


def add_role(request):
    if request.method == "POST":
        form = forms.RoleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Role added successfully")
            return redirect("company-settings")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error} in {field}")
                    print(f"{error} in {field}")
    else:
        form = forms.RoleForm()

    context = {
        "form": form,
    }
    return render(request, "settings.html", context)


def edit_role(request, role_id):
    role = get_object_or_404(models.Roles, id=role_id)
    print(role)
    if request.method == "POST":
        form = forms.EditRoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            messages.success(request, "Role updated successfully")
            return redirect("view_role", role_id=role.id)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error} in {field}")
    else:
        form = forms.EditRoleForm(instance=role)

    context = {
        "form": form,
        "role": role,
    }
    return render(request, "edit_role.html", context)


def delete_role(request, role_id):
    role = get_object_or_404(models.Roles, id=role_id)
    if request.method == "POST":
        role.delete()
        return redirect("list-of-roles")
    

def list_of_roles(request):
    roles = models.Role.objects.all()

    context = {
        "roles": roles,
    }
    return render(request, "list_of_roles.html", context)
