from django.contrib import admin
from .models import Attendance, Holiday


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ["employee", "date", "status", "in_time", "out_time", "working_hours"]
    list_filter = ["status", "date"]
    search_fields = ["employee__full_name", "employee__email"]


@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ["date", "name"]
    ordering = ["date"]