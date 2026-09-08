from django.urls import path
from . import views

app_name = "leaves"

urlpatterns = [
    path("apply/", views.apply_leave, name="apply"),
    path("my-leaves/", views.my_leaves, name="my_leaves"),
    path("history/", views.my_leave_history, name="history"),
    path("requests/", views.leave_requests_admin, name="admin_list"),
        path("employee/<int:pk>/history/", views.employee_leave_history, name="employee_history"),
    path("requests/<int:pk>/approve/", views.approve_leave, name="approve"),
    path("requests/<int:pk>/reject/", views.reject_leave, name="reject"),

    path("short-leave/apply/", views.apply_short_leave, name="apply_short_leave"),
    path("short-leave/my/", views.my_short_leaves, name="my_short_leaves"),
    path("short-leave/requests/", views.short_leave_requests_admin, name="short_leave_admin_list"),
    path("short-leave/requests/<int:pk>/approve/", views.approve_short_leave, name="approve_short_leave"),
    path("short-leave/requests/<int:pk>/reject/", views.reject_short_leave, name="reject_short_leave"),
]