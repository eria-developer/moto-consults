from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path('aggregate_earnings/<str:timeframe>/', views.aggregate_earnings, name='aggregate_earnings'),


    # customer urls 
    path("add-customer/", views.add_customer, name="add-customer"),
    path("edit-customer/<int:customer_id>/", views.edit_customer, name="edit-customer"),
    path("view-customer/<int:customer_id>/", views.view_customer, name="view-customer"),
    path("delete-customer/<int:customer_id>/", views.delete_customer, name="delete-customer"),
    path("list-of-customers/", views.list_of_customers, name="list-of-customers"),
    # path("search-customer/", views.search_customer, name="search-customer"),
    path('search_customers/', views.search_customers, name='search_customers'),

    # company urls 
    path("add-company/", views.add_company, name="add-company"),
    path("edit-company/<int:company_id>/", views.edit_company, name="edit-company"),
    path("view-company/<int:company_id>/", views.view_company, name="view-company"),
    path("delete-company/<int:company_id>/", views.delete_company, name="delete-company"),
    path("list-of-companies/", views.list_of_companies, name="list-of-companies"),
    # path('search_companies/', views.search_companies, name='search_companies'),

    # job urls 
    path("add-job/", views.add_job, name="add-job"),
    path("edit-job/<int:job_id>/", views.edit_job, name="edit-job"),
    path("view-job/<int:job_id>/", views.view_job, name="view-job"),
    path("delete-job/<int:job_id>/", views.delete_job, name="delete-job"),
    path("list-of-jobs/", views.list_of_jobs, name="list-of-jobs"),
    path('search_placements/', views.search_placements, name='search_placements'),

    # job position urls 
    path("add-jobposition/", views.add_jobposition, name="add-jobposition"),
    path("edit-jobposition/<int:jobposition_id>/", views.edit_jobposition, name="edit-jobposition"),
    path("view-jobposition/<int:jobposition_id>/", views.view_jobposition, name="view-jobposition"),
    path("delete-jobposition/<int:jobposition_id>/", views.delete_jobposition, name="delete-jobposition"),
    path("list-of-jobpositions/", views.list_of_jobpositions, name="list-of-jobpositions"),
    path("list-of-jobpositions/<int:job_position_id>", views.list_of_jobpositions, name="list-of-jobpositions"),
    # path("search-jobposition/", views.search_jobposition, name="search-jobposition"),

    # fee urls 
    path("add-fee/", views.add_fee, name="add-fee"),
    path("edit-fee/<int:fee_id>/", views.edit_fee, name="edit-fee"),
    path("view-fee/<int:fee_id>/", views.view_fee, name="view-fee"),
    path("delete-fee/<int:fee_id>/", views.delete_fee, name="delete-fee"),
    path("list-of-fees/", views.list_of_fees, name="list-of-fees"),
    path('preview_receipt/<int:fee_id>/', views.preview_receipt, name='preview_receipt'),
    path('generate_receipt/<int:fee_id>/', views.generate_receipt, name='generate_receipt'),



    # placement urls 
    path("add-placement/", views.add_placement, name="add-placement"),
    path("edit-placement/<int:placement_id>/", views.edit_placement, name="edit-placement"),
    path("view-placement/<int:placement_id>/", views.view_placement, name="view-placement"),
    path("delete-placement/<int:placement_id>/", views.delete_placement, name="delete-placement"),
    path("list-of-placements/", views.list_of_placements, name="list-of-placements"),
    # path("search-placement/", views.search_placement, name="search-placement"),

    # consultation urls 
    path("add-consultation/", views.add_consultation, name="add-consultation"),
    path("view-consultation/<int:consultation_id>/", views.view_consultation, name="view-consultation"),
    path("list-of-consultations/", views.list_of_consultations, name="list-of-consultations"),
    # path("search-placement/", views.search_placement, name="search-placement"),

    # settings urls 
    path("roles/", views.roles, name="roles"),
    path("company-settings/", views.company_settings, name="company-settings"),
    path("edit-settings/<int:id>", views.edit_settings, name="edit-settings"),
    path("my-profile/",views.my_profile, name="my-profile"),

    # expenses urls 
    path("add-expense/", views.add_expense, name="add-expense"),
    path("list-of-expenses/", views.list_of_expenses, name="list-of-expenses")
]
