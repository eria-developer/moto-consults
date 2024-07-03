from django.urls import path
from .views import  login_view, add_user, list_of_users

urlpatterns = [
    # path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),

    # user urls 
    path("add-user/", add_user, name="add-user"),
    path("list-of-users/", list_of_users, name="list-of-users"),
    # path("search-user/", views.search_user, name="search-user"),

] 

# urlpatterns += urls.urlpatterns
