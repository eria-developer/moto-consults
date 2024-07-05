from django.shortcuts import render, redirect, get_object_or_404
from . import models
from . import forms
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


@login_required(login_url="/")
def add_company(request):
    companies = models.EmployerCompany.objects.all().order_by("-date_added")

    if request.method == "POST":
        add_company_form = forms.CompanyForm(request.POST)
        if add_company_form.is_valid():
            add_company_form.save()
            messages.success(request, "Company added successfully")
            return redirect("list-of-companies")
        else:
            for field, errors in add_company_form.errors.items():
                for error in errors:
                    messages.error(request, f"{error} in {field}")
                    print(f"{error} in {field}")
    else:
        add_company_form = forms.CompanyForm()

    context = {
        "add_company_form": add_company_form,
        "companies": companies,
    }
    return render(request, "add_company.html", context)


@login_required(login_url="/")
def edit_company(request, company_id):
    company = get_object_or_404(models.EmployerCompany, id=company_id)
    # print(company)
    if request.method == "POST":
        form = forms.EditCompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, "Company details updated successfully")
            return redirect("list-of-companies")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error} in {field}")
    else:
        form = forms.EditCompanyForm(instance=company)

    context = {
        "form": form,
        "company": company,
    }
    return render(request, "edit_company.html", context)


@login_required(login_url="/")
def view_company(request, company_id):
    company = get_object_or_404(models.EmployerCompany, id=company_id)

    context = {
        "company": company,
    }
    return render(request, "view_company.html", context)


@login_required(login_url="/")
def delete_company(request, company_id):
    company = get_object_or_404(models.EmployerCompany, id=company_id)
    if request.method == "POST":
        company.delete()
        return redirect("list-of-companies")
    

@login_required(login_url="/")
def list_of_companies(request):
    if 'edit_id' in request.GET:
        company_id = request.GET['edit_id']
        company = get_object_or_404(models.EmployerCompany, pk=company_id)
        edit_company_form = forms.EditCompanyForm(instance=company)
    else:
        edit_company_form = forms.EditCompanyForm()
        companies = models.EmployerCompany.objects.all().order_by("-date_added")

    if request.method == 'POST':
        form_name = request.POST.get('form_name')
        if form_name == "edit_company_form":
            company_id = request.POST.get('company_id')
            company = get_object_or_404(models.EmployerCompany, pk=company_id)
            edit_company_form = forms.EditCompanyForm(request.POST, instance=company)
            if edit_company_form.is_valid():
                edit_company_form.save()
                messages.success(request, "Company updated successfully!")
                return redirect('list-of-companies')
        elif form_name == "add_company_form":
            add_company_form = forms.CompanyForm(request.POST)
            if add_company_form.is_valid():
                add_company_form.save()
                messages.success(request, "Company added successfully!")
                return redirect('list-of-companies')
    
    add_company_form = forms.CompanyForm()
    context = {
        "companies": companies,
        "edit_company_form": edit_company_form,
        "add_company_form": add_company_form
    }
    return render(request, "list_of_companies.html", context)


@login_required(login_url="/")
def search_companies(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        query = request.GET.get("query", "")
        companies = models.EmployerCompany.objects.filter(
            Q(name__icontains=query) |
            Q(phone_number = query) |
            Q(address__icontains=query) |
            Q(email__icontains = query)
        ).order_by("-date_added")

        company_list = []
        for company in companies:
            company_data = {
                "id": company.id,
                 "name": company.name,
                "phone_number": company.phone_number,
                "email": company.email,
                "address": company.address,
                "date_added": company.date_added.strftime("%Y-%m-%d %H:%M:%S"),
                "description": company.description,
                "view_url": reverse('view-company', args=[company.id]),
                "edit_url": reverse('edit-company', args=[company.id]),
                "delete_url": reverse('delete-company', args=[company.id]),
            }
            company_list.append(company_data)

        return JsonResponse({"companies": company_list})
    return JsonResponse({"companies": []})