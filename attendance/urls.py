from django.urls import path
from . import views

app_name = "attendance"

urlpatterns = [
    path("my-attendance/", views.my_attendance, name="my_attendance"),
    path("punch-in/", views.punch_in, name="punch_in"),
    path("punch-out/", views.punch_out, name="punch_out"),
    path("records/", views.attendance_admin_list, name="admin_list"),
    path("holidays/", views.holiday_list, name="holidays"),
]