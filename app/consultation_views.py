from django.shortcuts import render, redirect, get_object_or_404
from . import models
from . import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(login_url="/")
def add_consultation(request):
    if request.method == "POST":
        form = forms.ConsultationForm(request.POST)
        if form.is_valid():
            print(form)
            form.save()
            messages.success(request, "consultation instance added successfully")
            return redirect("list-of-consultations")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error} in {field}")
                    print(f"{error} in {field}")
    else:
        form = forms.ConsultationForm()


    context = {
        "form": form,
    }
    return render(request, "add_consultation.html", context)


@login_required(login_url="/")
def view_consultation(request, consultation_id):
    consultation = get_object_or_404(models.Consultation, id=consultation_id)

    context = {
        "consultation": consultation,
    }
    return render(request, "view_consultation.html", context)


@login_required(login_url="/")
def list_of_consultations(request):
    consultation = models.Consultation.objects.all().order_by("-consultation_date")

    context = {
        "consultation": consultation,
    }
    return render(request, "list_of_consultations.html", context)