import csv

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from leaves.models import LeaveRequest, ShortLeaveRequest
from accounts.models import User


def is_admin(user):
    return user.is_authenticated and user.is_admin_role()


def _build_combined(request):
    employee_id = request.GET.get("employee")
    leave_type = request.GET.get("leave_type")
    status = request.GET.get("status")
    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")

    combined = []

    if not leave_type or leave_type != "Short Leave":
        qs = LeaveRequest.objects.select_related("employee").order_by("-applied_at")
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

        for lr in qs:
            combined.append({
                "employee_name": lr.employee.full_name,
                "employee_email": lr.employee.email,
                "kind": "Full Leave",
                "type_label": lr.leave_type,
                "from_display": lr.from_date,
                "to_display": lr.to_date,
                "amount": f"{lr.total_days} day(s)",
                "status": lr.status,
                "applied_at": lr.applied_at,
                "manager_remark": lr.manager_remark,
                "slip_url_name": "reports:leave_slip",
                "pk": lr.pk,
            })

    if not leave_type or leave_type == "Short Leave":
        sqs = ShortLeaveRequest.objects.select_related("employee").order_by("-applied_at")
        if employee_id:
            sqs = sqs.filter(employee_id=employee_id)
        if status:
            sqs = sqs.filter(status=status)
        if from_date:
            sqs = sqs.filter(date__gte=from_date)
        if to_date:
            sqs = sqs.filter(date__lte=to_date)

        for sl in sqs:
            combined.append({
                "employee_name": sl.employee.full_name,
                "employee_email": sl.employee.email,
                "kind": "Short Leave",
                "type_label": "Short Leave",
                "from_display": sl.date,
                "to_display": f"{sl.from_time.strftime('%I:%M %p')} - {sl.to_time.strftime('%I:%M %p')}",
                "amount": f"{sl.duration_hours} hr(s)",
                "status": sl.status,
                "applied_at": sl.applied_at,
                "manager_remark": sl.manager_remark,
                "slip_url_name": "reports:short_leave_slip",
                "pk": sl.pk,
            })

    combined.sort(key=lambda x: x["applied_at"], reverse=True)
    return combined


@login_required
@user_passes_test(is_admin, login_url="accounts:login")
def leave_reports(request):
    combined = _build_combined(request)
    employees = User.objects.filter(role="employee").order_by("full_name")
    leave_types = list(LeaveRequest.LEAVE_TYPE_CHOICES) + [("Short Leave", "Short Leave")]
    statuses = LeaveRequest.STATUS_CHOICES
    return render(request, "reports/leave_reports.html", {
        "combined": combined,
        "employees": employees,
        "leave_types": leave_types,
        "statuses": statuses,
        "query": request.GET,
    })


@login_required
@user_passes_test(is_admin, login_url="accounts:login")
def export_leave_csv(request):
    combined = _build_combined(request)

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="leave_report.csv"'

    writer = csv.writer(response)
    writer.writerow(["Employee", "Email", "Kind", "Type", "From", "To", "Amount", "Status", "Applied On", "Manager Remark"])
    for item in combined:
        writer.writerow([
            item["employee_name"],
            item["employee_email"],
            item["kind"],
            item["type_label"],
            item["from_display"],
            item["to_display"],
            item["amount"],
            item["status"],
            item["applied_at"].strftime("%Y-%m-%d %H:%M"),
            item["manager_remark"],
        ])
    return response


@login_required
def leave_slip(request, pk):
    leave = get_object_or_404(LeaveRequest, pk=pk, status="Approved")
    if not request.user.is_admin_role() and leave.employee_id != request.user.id:
        return HttpResponse("Not authorized to view this slip.", status=403)
    return render(request, "reports/leave_slip.html", {"leave": leave})


@login_required
def short_leave_slip(request, pk):
    leave = get_object_or_404(ShortLeaveRequest, pk=pk, status="Approved")
    if not request.user.is_admin_role() and leave.employee_id != request.user.id:
        return HttpResponse("Not authorized to view this slip.", status=403)
    return render(request, "reports/short_leave_slip.html", {"leave": leave})