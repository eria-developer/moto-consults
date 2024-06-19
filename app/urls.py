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
    # path("add-company/", views.add_company, name="add-company"),
    # path("edit-company/<int:company_id>/", views.edit_company, name="edit-company"),
    # path("view-company/<int:company_id>/", views.view_company, name="view-company"),
    # path("delete-company/<int:company_id>/", views.delete_company, name="delete-company"),
    # path("list-of-companies/", views.list_of_companies, name="list-of-companies"),
    # path("search-company/", views.search_company, name="search-company"),
]
