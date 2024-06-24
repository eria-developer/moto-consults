from django.shortcuts import render, redirect, get_object_or_404
from . import models
from . import forms
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse
from django.http import JsonResponse



def add_placement(request):
    if request.method == "POST":
        form = forms.PlacementForm(request.POST)
        if form.is_valid():
            print(form)
            form.save()
            messages.success(request, "Placement added successfully")
            return redirect("list-of-placements")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error} in {field}")
                    print(f"Erros are: {error} in {field}")
    else:
        form = forms.PlacementForm()

    customers = models.Customer.objects.all()
    jobs = models.Job.objects.all()
    status_choices = models.RecruitmentProcess.STATUS_CHOICES
    job_companies = models.EmployerCompany.objects.all()

    context = {
        "form": form,
        "customers": customers,
        "jobs": jobs,
        "status_choices": status_choices,
        "job_companies": job_companies,
    }
    return render(request, "add_placement.html", context)


def edit_placement(request, placement_id):
    placement = get_object_or_404(models.RecruitmentProcess, id=placement_id)
    print(placement)
    if request.method == "POST":
        form = forms.EditPlacementForm(request.POST, instance=placement)
        if form.is_valid():
            form.save()
            messages.success(request, "placement details updated successfully")
            return redirect("view_placement", placement_id=placement.id)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error} in {field}")
    else:
        form = forms.EditPlacementForm(instance=placement)

    context = {
        "form": form,
        "placement": placement,
    }
    return render(request, "edit_placement.html", context)


def view_placement(request, placement_id):
    placement = get_object_or_404(models.RecruitmentProcess, id=placement_id)

    context = {
        "placement": placement,
    }
    return render(request, "view_placement.html", context)


def delete_placement(request, placement_id):
    placement = get_object_or_404(models.RecruitmentProcess, id=placement_id)
    if request.method == "POST":
        placement.delete()
        return redirect("list-of-placements")
    

def list_of_placements(request):
    placements = models.RecruitmentProcess.objects.all()

    context = {
        "placements": placements,
    }
    return render(request, "list_of_placements.html", context)


def search_placements(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        query = request.GET.get("query", "")
        placements = models.RecruitmentProcess.objects.filter(
            Q(customer__firstname__icontains=query) |
            Q(customer__othernames__icontains=query) |
            Q(job__job_title__icontains=query) |
            Q(job__job_company__job_title__icontains=query) |
            Q(status__icontains=query)
        ).order_by("-application_date")

        placement_list = []
        for placement in placements:
            placement_data = {
                "fullname": f"{placement.customer.firstname} {placement.customer.othernames}",
                "job": placement.job.job_title,
                "company": placement.job.job_company.job_title if placement.job.job_company else "",
                "status": placement.status,
                "view_url": reverse('view-placement', args=[placement.id]),
                "edit_url": reverse('edit-placement', args=[placement.id]),
                "delete_url": reverse('delete-placement', args=[placement.id]),
            }
            placement_list.append(placement_data)

        return JsonResponse({"placements": placement_list})
    return JsonResponse({"placements": []})