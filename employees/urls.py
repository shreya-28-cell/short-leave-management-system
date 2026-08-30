from django.urls import path
from . import views

app_name = "employees"

urlpatterns = [
    path("", views.employee_list, name="list"),
    path("add/", views.employee_add, name="add"),
    path("toggle/<int:pk>/", views.employee_toggle_active, name="toggle_active"),
    path("delete/<int:pk>/", views.employee_delete, name="delete"),
    path("my-profile/", views.my_profile, name="profile"),
]