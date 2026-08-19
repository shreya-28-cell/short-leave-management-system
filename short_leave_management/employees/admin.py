from django.contrib import admin
from .models import EmployeeProfile


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'user', 'department', 'designation')
    search_fields = ('employee_id', 'user__username', 'user__first_name')