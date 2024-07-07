from django.shortcuts import render, redirect, get_object_or_404
from . import models
from . import forms
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


@login_required(login_url="/")
def add_placement(request):
    if request.method == "POST":
        form_name = request.POST.get('form_name')

        if form_name == "add_placement_form":
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
        
        elif form_name == "add_customer_form":
            form = forms.CustomerForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Customer added successfully")
                return redirect("add-placement")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{error} in {field}")

        elif form_name == "add_company_form":
            add_company_form = forms.CompanyForm(request.POST)
            if add_company_form.is_valid():
                add_company_form.save()
                messages.success(request, "Company added successfully")
                return redirect("add-placement")
            else:
                for field, errors in add_company_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{error} in {field}")
                        print(f"{error} in {field}")
        elif form_name == "add_job_form":
            add_job_form = forms.JobForm(request.POST)
            if add_job_form.is_valid():
                add_job_form.save()
                messages.success(request, "Job added successfully")
                return redirect("add-placement")
            else:
                for field, errors in add_job_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{error} in {field}")
                        print(f"{error} in {field}")
    else:
        add_placement_form = forms.PlacementForm()
        add_customer_form = forms.CustomerForm()
        add_job_form = forms.JobForm()
        add_company_form = forms.CompanyForm()

    customers = models.Customer.objects.all()
    jobs = models.Job.objects.all()
    status_choices = models.RecruitmentProcess.STATUS_CHOICES
    job_companies = models.EmployerCompany.objects.all()

    context = {
        "add_placement_form": add_placement_form,
        "add_customer_form": add_customer_form,
        "add_job_form": add_job_form,
        "add_company_form": add_company_form,
        "customers": customers,
        "jobs": jobs,
        "status_choices": status_choices,
        "job_companies": job_companies,
    }
    # print(f"Context {context}")
    return render(request, "add_placement.html", context)


@login_required(login_url="/")
def edit_placement(request, placement_id):
    placement = get_object_or_404(models.RecruitmentProcess, id=placement_id)
    
    if request.method == "POST":
        form = forms.EditPlacementForm(request.POST, instance=placement)
        if form.is_valid():
            # Get related objects and ensure they are correctly assigned
            customer_id = request.POST.get("customer")
            job_id = request.POST.get("job")
            company_id = request.POST.get("company")
            
            if customer_id:
                customer = get_object_or_404(models.Customer, id=customer_id)
            else:
                customer = None
                
            if job_id:
                job = get_object_or_404(models.Job, id=job_id)
            else:
                job = None

            if company_id:
                company = get_object_or_404(models.EmployerCompany, id=company_id)
            else:
                company = None

            placement.customer = customer
            placement.job = job
            placement.company = company
            placement.status = request.POST.get("status")
            placement.expected_salary = request.POST.get("expected_salary")

            placement.save()
            print(f"Placement: {placement}")
            messages.success(request, f"'{placement.customer.firstname}'s placement updated successfully.")
            return redirect("list-of-placements")
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


@login_required(login_url="/")
def view_placement(request, placement_id):
    placement = get_object_or_404(models.RecruitmentProcess, id=placement_id)

    context = {
        "placement": placement,
    }
    return render(request, "view_placement.html", context)


@login_required(login_url="/")
def delete_placement(request, placement_id):
    placement = get_object_or_404(models.RecruitmentProcess, id=placement_id)
    if request.method == "POST":
        placement.delete()
        messages.success(request, f"{placement.job.job_title} has been deleted successfully")
        return redirect("list-of-placements")
    

@login_required(login_url="/")
def list_of_placements(request):
    placements = models.RecruitmentProcess.objects.all()
    customers = models.Customer.objects.all()
    jobs = models.Job.objects.all()
    status_choices = models.RecruitmentProcess.STATUS_CHOICES
    job_companies = models.EmployerCompany.objects.all()

    context = {
        "placements": placements,
        "customers": customers,
        "jobs": jobs,
        "status_choices": status_choices,
        "job_companies": job_companies,
    }
    return render(request, "list_of_placements.html", context)


@login_required(login_url="/")
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