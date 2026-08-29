from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.utils import timezone
from accounts.models import User
from leaves.models import LeaveRequest, LeaveBalance
from attendance.models import Attendance


def is_admin(user):
    return user.is_authenticated and user.is_admin_role()


def is_employee(user):
    return user.is_authenticated and user.is_employee_role()


@login_required
@user_passes_test(is_admin, login_url="accounts:login")
def admin_dashboard(request):
    employee_count = User.objects.filter(role="employee").count()
    pending_leaves_count = LeaveRequest.objects.filter(status="Pending").count()
    present_today_count = Attendance.objects.filter(date=timezone.localdate(), status="Present").count()
    return render(request, "dashboard/admin_dashboard.html", {
        "employee_count": employee_count,
        "pending_leaves_count": pending_leaves_count,
        "present_today_count": present_today_count,
    })


@login_required
@user_passes_test(is_employee, login_url="accounts:login")
def employee_dashboard(request):
    balance, _ = LeaveBalance.objects.get_or_create(user=request.user)
    today_record = Attendance.objects.filter(employee=request.user, date=timezone.localdate()).first()
    return render(request, "dashboard/employee_dashboard.html", {
        "balance": balance,
        "today_record": today_record,
    })