from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from . import models
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

    role_choices = models.CustomUser.ROLE_CHOICES

    context = {
        'form': form,
        "role_choices": role_choices,
        }
    return render(request, 'add_user.html', context)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('list-of-customers')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def list_of_users(request):
    users = models.CustomUser.objects.all()

    context = {
        "users": users,
    }
    return render(request, "list_of_users.html", context)

