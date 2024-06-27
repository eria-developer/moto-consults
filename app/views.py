from .customer_views import dashboard, add_customer, edit_customer, view_customer, delete_customer, list_of_customers, search_customers
from .company_views import add_company, edit_company, view_company, delete_company, list_of_companies
from .job_views import add_job, edit_job, view_job, delete_job, list_of_jobs
from .jobposition_views import add_jobposition, edit_jobposition, view_jobposition, delete_jobposition, list_of_jobpositions
from .fee_views import add_fee, edit_fee, view_fee, delete_fee, list_of_fees, generate_receipt, preview_receipt
from .placement_views import add_placement, edit_placement, view_placement, delete_placement, list_of_placements, search_placements
from .consultation_views import add_consultation, view_consultation, list_of_consultations
from .settings_views import company_settings, roles, my_profile, edit_settings

from django.shortcuts import render
from . import models
from authentication.models import CustomUser

def dashboard(request):
    total_customers = models.Customer.objects.count()
    total_companies = models.EmployerCompany.objects.count()
    total_jobs = models.Job.objects.count()
    total_placements = models.RecruitmentProcess.objects.count()
    
    context = {
        "total_customers": total_customers,
        "total_companies": total_companies,
        "total_jobs": total_jobs,
        "total_placements": total_placements,
    }
    return render(request, "dashboard.html", context)