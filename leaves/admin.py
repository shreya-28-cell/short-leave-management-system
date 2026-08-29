from django.contrib import admin
from .models import LeaveBalance, LeaveRequest


@admin.register(LeaveBalance)
class LeaveBalanceAdmin(admin.ModelAdmin):
    list_display = ["user", "casual_leave", "used_casual_leave", "sick_leave", "used_sick_leave", "paid_leave", "used_paid_leave"]
    search_fields = ["user__full_name", "user__email"]


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ["employee", "leave_type", "from_date", "to_date", "total_days", "status", "applied_at"]
    list_filter = ["status", "leave_type"]
    search_fields = ["employee__full_name", "employee__email"]
