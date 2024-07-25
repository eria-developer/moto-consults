from django.urls import path
from .views import  login_view, add_user, list_of_users, view_user, delete_user, edit_user,edit_profile, view_profile, CustomPasswordChangeView, CustomPasswordChangeDoneView



urlpatterns = [
    # path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),

    # user urls 
    path("add-user/", add_user, name="add-user"),
    path("list-of-users/", list_of_users, name="list-of-users"),
    path("edit-user/<int:user_id>", edit_user, name="edit-user"),
    path("view-user/<int:user_id>", view_user, name="view-user"),
    path("delete-user/<int:user_id>", delete_user, name="delete-user"),
    path('profile/', view_profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    # path("search-user/", views.search_user, name="search-user"),

    # changing passwords
    path('password-change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', CustomPasswordChangeDoneView.as_view(), name='password_change_done'),


] 

# urlpatterns += urls.urlpatterns
