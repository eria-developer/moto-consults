from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),

    # customer urls 
    path("add-customer/", views.add_customer, name="add-customer"),
    path("edit-customer/<int:customer_id>/", views.edit_customer, name="edit-customer"),
    path("view-customer/<int:customer_id>/", views.view_customer, name="view-customer"),
    path("delete-customer/<int:customer_id>/", views.delete_customer, name="delete-customer"),
    path("list-of-customers/", views.list_of_customers, name="list-of-customers"),
    path("search-customer/", views.search_customer, name="search-customer"),

    # company urls 
    path("add-company/", views.add_company, name="add-company"),
    path("edit-company/<int:company_id>/", views.edit_company, name="edit-company"),
    path("view-company/<int:company_id>/", views.view_company, name="view-company"),
    path("delete-company/<int:company_id>/", views.delete_company, name="delete-company"),
    path("list-of-companies/", views.list_of_companies, name="list-of-companies"),
    # path("search-company/", views.search_company, name="search-company"),

    # job urls 
    path("add-job/", views.add_job, name="add-job"),
    path("edit-job/<int:job_id>/", views.edit_job, name="edit-job"),
    path("view-job/<int:job_id>/", views.view_job, name="view-job"),
    path("delete-job/<int:job_id>/", views.delete_job, name="delete-job"),
    path("list-of-jobs/", views.list_of_jobs, name="list-of-jobs"),
    # path("search-job/", views.search_job, name="search-job"),

    # job position urls 
    path("add-jobposition/", views.add_jobposition, name="add-jobposition"),
    path("edit-jobposition/<int:jobposition_id>/", views.edit_jobposition, name="edit-jobposition"),
    path("view-jobposition/<int:jobposition_id>/", views.view_jobposition, name="view-jobposition"),
    path("delete-jobposition/<int:jobposition_id>/", views.delete_jobposition, name="delete-jobposition"),
    path("list-of-jobpositions/", views.list_of_jobpositions, name="list-of-jobpositions"),
    # path("search-jobposition/", views.search_jobposition, name="search-jobposition"),
]
