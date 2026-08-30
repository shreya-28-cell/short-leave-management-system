import csv

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from leaves.models import LeaveRequest
from accounts.models import User


def is_admin(user):
    return user.is_authenticated and user.is_admin_role()


def _filtered_queryset(request):
    qs = LeaveRequest.objects.select_related("employee").order_by("-applied_at")

    employee_id = request.GET.get("employee")
    leave_type = request.GET.get("leave_type")
    status = request.GET.get("status")
    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")

    if employee_id:
        qs = qs.filter(employee_id=employee_id)
    if leave_type:
        qs = qs.filter(leave_type=leave_type)
    if status:
        qs = qs.filter(status=status)
    if from_date:
        qs = qs.filter(from_date__gte=from_date)
    if to_date:
        qs = qs.filter(to_date__lte=to_date)

    return qs


@login_required
@user_passes_test(is_admin, login_url="accounts:login")
def leave_reports(request):
    leave_requests = _filtered_queryset(request)
    employees = User.objects.filter(role="employee").order_by("full_name")
    return render(request, "reports/leave_reports.html", {
        "leave_requests": leave_requests,
        "employees": employees,
        "leave_types": LeaveRequest.LEAVE_TYPE_CHOICES,
        "statuses": LeaveRequest.STATUS_CHOICES,
        "query": request.GET,
    })


@login_required
@user_passes_test(is_admin, login_url="accounts:login")
def export_leave_csv(request):
    leave_requests = _filtered_queryset(request)

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="leave_report.csv"'

    writer = csv.writer(response)
    writer.writerow(["Employee", "Email", "Leave Type", "From", "To", "Days", "Status", "Applied On", "Manager Remark"])
    for lr in leave_requests:
        writer.writerow([
            lr.employee.full_name,
            lr.employee.email,
            lr.leave_type,
            lr.from_date,
            lr.to_date,
            lr.total_days,
            lr.status,
            lr.applied_at.strftime("%Y-%m-%d %H:%M"),
            lr.manager_remark,
        ])
    return response


@login_required
def leave_slip(request, pk):
    leave = get_object_or_404(LeaveRequest, pk=pk, status="Approved")
    if not request.user.is_admin_role() and leave.employee_id != request.user.id:
        return HttpResponse("Not authorized to view this slip.", status=403)
    return render(request, "reports/leave_slip.html", {"leave": leave})