from django.shortcuts import render, redirect, get_object_or_404
from . import models
from . import forms
from django.contrib import messages



def add_job(request):
    job_positions = models.JobPosition.objects.all()

    if request.method == "POST":
        add_job_form = forms.JobForm(request.POST)
        if add_job_form.is_valid():
            add_job_form.save()
            messages.success(request, "Job added successfully")
            return redirect("list-of-jobs")
        else:
            for field, errors in add_job_form.errors.items():
                for error in errors:
                    messages.error(request, f"{error} in {field}")
                    print(f"{error} in {field}")
    else:
        add_job_form = forms.JobForm()

    context = {
        "add_job_form": add_job_form,
        "job_positions": job_positions,
    }
    return render(request, "add_job.html", context)


def edit_job(request, job_id):
    job = get_object_or_404(models.Job, id=job_id)
    print(job)
    if request.method == "POST":
        form = forms.EditJobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job details updated successfully")
            return redirect("list-of-jobs")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error} in {field}")
    else:
        form = forms.EditJobForm(instance=job)

    context = {
        "form": form,
        "job": job,
    }
    return render(request, "edit_job.html", context)


def view_job(request, job_id):
    job = get_object_or_404(models.Job, id=job_id)

    context = {
        "job": job,
    }
    return render(request, "view_job.html", context)


def delete_job(request, job_id):
    job = get_object_or_404(models.Job, id=job_id)
    if request.method == "POST":
        job.delete()
        return redirect("list-of-jobs")
    

def list_of_jobs(request):
    if 'edit_id' in request.GET:
        job_id = request.GET['edit_id']
        job = get_object_or_404(models.Job, pk=job_id)
        edit_job_form = forms.EditJobForm(instance=job)
    else:
        edit_job_form = forms.EditJobForm()
        jobs = models.Job.objects.all()

    if request.method == 'POST':
        form_name = request.POST.get('form_name')
        if form_name == "edit_job_form":
            job_id = request.POST.get('job_id')
            job = get_object_or_404(models.Job, pk=job_id)
            edit_job_form = forms.EditJobForm(request.POST, instance=job)
            if edit_job_form.is_valid():
                edit_job_form.save()
                messages.success(request, "Job updated successfully!")
                return redirect('list-of-jobs')
        elif form_name == "add_job_form":
            add_job_form = forms.JobForm(request.POST)
            if add_job_form.is_valid():
                add_job_form.save()
                messages.success(request, "Job added successfully!")
                return redirect('list-of-jobs')
    
    add_job_form = forms.JobForm()
    context = {
        "jobs": jobs,
        "edit_job_form": edit_job_form,
        "add_job_form": add_job_form
    }
    return render(request, "list_of_jobs.html", context)
