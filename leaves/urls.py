from django.urls import path
from . import views

app_name = "leaves"

urlpatterns = [
    path("apply/", views.apply_leave, name="apply"),
    path("my-leaves/", views.my_leaves, name="my_leaves"),
    path("requests/", views.leave_requests_admin, name="admin_list"),
    path("requests/<int:pk>/approve/", views.approve_leave, name="approve"),
    path("requests/<int:pk>/reject/", views.reject_leave, name="reject"),
]
