from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from . import models
from . import forms
from django.contrib import messages



def add_company(request):
    if request.method == "POST":
        form = forms.CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Company added successfully")
            return redirect("list-of-companies")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error} in {field}")
    else:
        form = forms.CompanyForm()

    context = {
        "form": form,
    }
    return render(request, "add_company.html", context)


def edit_company(request, company_id):
    company = get_object_or_404(models.EmployerCompany, id=company_id)
    print(company)
    if request.method == "POST":
        form = forms.EditCompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, "company details updated successfully")
            return redirect("view_company", company_id=company.id)
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


def view_company(request, company_id):
    company = get_object_or_404(models.EmployerCompany, id=company_id)

    context = {
        "company": company,
    }
    return render(request, "view_company.html", context)


def delete_company(request, company_id):
    company = get_object_or_404(models.EmployerCompany, id=company_id)
    if request.method == "POST":
        company.delete()
        return redirect("list-of-companies")
    

def list_of_companies(request):
    companies = models.EmployerCompany.objects.all()

    context = {
        "companies": companies,
    }
    return render(request, "list_of_companies.html", context)
