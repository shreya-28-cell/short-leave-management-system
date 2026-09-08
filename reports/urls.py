from django.urls import path
from . import views

app_name = "reports"

urlpatterns = [
    path("leaves/", views.leave_reports, name="leave_reports"),
    path("leaves/export/", views.export_leave_csv, name="export_leave_csv"),
    path("slip/<int:pk>/", views.leave_slip, name="leave_slip"),
    path("slip/short/<int:pk>/", views.short_leave_slip, name="short_leave_slip"),
]