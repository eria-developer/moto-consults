from django.shortcuts import render, redirect, get_object_or_404
from . import models
from . import forms
from django.contrib import messages



def add_jobposition(request):
    if request.method == "POST":
        form = forms.JobpositionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Job position added successfully")
            return redirect("list-of-jobpositions")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error} in {field}")
                    print(f"{error} in {field}")
    else:
        form = forms.JobpositionForm()

    context = {
        "form": form,
    }
    return render(request, "add_jobposition.html", context)


def edit_jobposition(request, jobposition_id):
    jobposition = get_object_or_404(models.JobPosition, id=jobposition_id)
    print(jobposition)
    if request.method == "POST":
        form = forms.EditJobpositionForm(request.POST, instance=jobposition)
        if form.is_valid():
            form.save()
            messages.success(request, "Job position details updated successfully")
            return redirect("view_jobposition", jobposition_id=jobposition.id)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error} in {field}")
    else:
        form = forms.EditJobpositionForm(instance=jobposition)

    context = {
        "form": form,
        "jobposition": jobposition,
    }
    return render(request, "edit_jobposition.html", context)


def view_jobposition(request, jobposition_id):
    jobposition = get_object_or_404(models.JobPosition, id=jobposition_id)

    context = {
        "jobposition": jobposition,
    }
    return render(request, "view_jobposition.html", context)


def delete_jobposition(request, jobposition_id):
    jobposition = get_object_or_404(models.JobPosition, id=jobposition_id)
    if request.method == "POST":
        jobposition.delete()
        return redirect("list-of-jobpositions")
    

def list_of_jobpositions(request):
    jobpositions = models.JobPosition.objects.all()

    context = {
        "jobpositions": jobpositions,
    }
    return render(request, "list_of_jobpositions.html", context)
