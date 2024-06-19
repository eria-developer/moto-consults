from django.shortcuts import render, redirect, get_object_or_404
from . import models
from . import forms
from django.contrib import messages



def add_job(request):
    if request.method == "POST":
        form = forms.JobForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Job added successfully")
            return redirect("list-of-jobs")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error} in {field}")
    else:
        form = forms.JobForm()

    context = {
        "form": form,
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
            return redirect("view_job", job_id=job.id)
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
    jobs = models.Job.objects.all()

    context = {
        "jobs": jobs,
    }
    return render(request, "list_of_jobs.html", context)
