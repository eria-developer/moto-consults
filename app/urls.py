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
]
