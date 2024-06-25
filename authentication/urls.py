from django.urls import path
from .views import  login_view, add_user, list_of_users
# edit_user, view_user, delete_user, 

urlpatterns = [
    # path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),

    # user urls 
    path("add-user/", add_user, name="add-user"),
    # path("edit-user/<int:user_id>/", views.edit_user, name="edit-user"),
    # path("view-user/<int:user_id>/", views.view_user, name="view-user"),
    # path("delete-user/<int:user_id>/", views.delete_user, name="delete-user"),
    path("list-of-users/", list_of_users, name="list-of-users"),
    # path("search-user/", views.search_user, name="search-user"),
]
