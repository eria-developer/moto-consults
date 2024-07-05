from django.shortcuts import render, redirect, get_object_or_404
from . import models
from . import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(login_url="/")
def add_jobposition(request):
    if request.method == "POST":
        add_job_position_form = forms.JobpositionForm(request.POST)
        if add_job_position_form.is_valid():
            add_job_position_form.save()
            messages.success(request, "Job position added successfully")
            return redirect("list-of-jobpositions")
        else:
            for field, errors in add_job_position_form.errors.items():
                for error in errors:
                    messages.error(request, f"{error} in {field}")
                    print(f"{error} in {field}")
    else:
        add_job_position_form = forms.JobpositionForm()

    context = {
        "add_job_position_form": add_job_position_form,
    }
    return render(request, "add_jobposition.html", context)


@login_required(login_url="/")
def edit_jobposition(request, jobposition_id):
    jobposition = get_object_or_404(models.JobPosition, id=jobposition_id)
    print(jobposition)
    if request.method == "POST":
        form = forms.EditJobpositionForm(request.POST, instance=jobposition)
        if form.is_valid():
            form.save()
            messages.success(request, "Job position details updated successfully")
            return redirect("list-of-jobpositions")
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


@login_required(login_url="/")
def view_jobposition(request, jobposition_id):
    jobposition = get_object_or_404(models.JobPosition, id=jobposition_id)

    context = {
        "jobposition": jobposition,
    }
    return render(request, "view_jobposition.html", context)


@login_required(login_url="/")
def delete_jobposition(request, jobposition_id):
    jobposition = get_object_or_404(models.JobPosition, id=jobposition_id)
    if request.method == "POST":
        jobposition.delete()
        messages.success(request, f"{jobposition.job_position} has been deleted successfully.")
        return redirect("list-of-jobpositions")
    

@login_required(login_url="/")
def list_of_jobpositions(request):
    if 'edit_id' in request.GET:
        job_position_id = request.GET['edit_id']
        job_position = get_object_or_404(models.JobPosition, pk=job_position_id)
        edit_job_position_form = forms.EditJobpositionForm(instance=job_position)
    else:
        edit_job_position_form = forms.EditJobpositionForm()
        jobpositions = models.JobPosition.objects.all()

    if request.method == 'POST':
        form_name = request.POST.get('form_name')
        if form_name == "edit_job_position_form":
            job_position_id = request.POST.get('job_position_id')
            job_position = get_object_or_404(models.JobPosition, pk=job_position_id)
            edit_job_position_form = forms.EditJobpositionForm(request.POST, instance=job_position)
            if edit_job_position_form.is_valid():
                edit_job_position_form.save()
                messages.success(request, "Job position updated successfully!")
                return redirect('list-of-jobpositions')
        elif form_name == "add_job_position_form":
            add_job_position_form = forms.JobpositionForm(request.POST)
            if add_job_position_form.is_valid():
                add_job_position_form.save()
                messages.success(request, "Job position added successfully!")
                return redirect('list-of-jobpositions')
    
    add_job_position_form = forms.JobpositionForm()
    context = {
        "jobpositions": jobpositions,
        "edit_job_position_form": edit_job_position_form,
        "add_job_position_form": add_job_position_form
    }
    return render(request, "list_of_jobpositions.html", context)
