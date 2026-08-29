from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db.models import Case, When, Value, IntegerField

from .models import LeaveRequest, LeaveBalance
from .forms import LeaveApplicationForm


def is_admin(user):
    return user.is_authenticated and user.is_admin_role()


def is_employee(user):
    return user.is_authenticated and user.is_employee_role()


# ---------- Employee views ----------

@login_required
@user_passes_test(is_employee, login_url="accounts:login")
def apply_leave(request):
    if request.method == "POST":
        form = LeaveApplicationForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = request.user
            leave.total_days = (leave.to_date - leave.from_date).days + 1
            leave.save()
            LeaveBalance.objects.get_or_create(user=request.user)
            messages.success(request, "Leave request submitted.")
            return redirect("leaves:my_leaves")
    else:
        form = LeaveApplicationForm()
    return render(request, "leaves/apply.html", {"form": form})


@login_required
@user_passes_test(is_employee, login_url="accounts:login")
def my_leaves(request):
    balance, _ = LeaveBalance.objects.get_or_create(user=request.user)
    leave_requests = request.user.leave_requests.all()
    return render(request, "leaves/my_leaves.html", {"leave_requests": leave_requests, "balance": balance})


# ---------- Admin views ----------

@login_required
@user_passes_test(is_admin, login_url="accounts:login")
def leave_requests_admin(request):
    leave_requests = (
        LeaveRequest.objects.select_related("employee")
        .annotate(
            priority=Case(
                When(status="Pending", then=Value(0)),
                default=Value(1),
                output_field=IntegerField(),
            )
        )
        .order_by("priority", "-applied_at")
    )
    return render(request, "leaves/admin_list.html", {"leave_requests": leave_requests})


def _remaining_for(balance, leave_type):
    if leave_type == "Casual Leave":
        return balance.remaining_casual
    if leave_type == "Sick Leave":
        return balance.remaining_sick
    return balance.remaining_paid


def _deduct_for(balance, leave_type, days):
    if leave_type == "Casual Leave":
        balance.used_casual_leave += days
    elif leave_type == "Sick Leave":
        balance.used_sick_leave += days
    else:
        balance.used_paid_leave += days


@login_required
@user_passes_test(is_admin, login_url="accounts:login")
@require_POST
def approve_leave(request, pk):
    leave = get_object_or_404(LeaveRequest, pk=pk)

    if leave.status != "Pending":
        messages.warning(request, "This request has already been processed.")
        return redirect("leaves:admin_list")

    balance, _ = LeaveBalance.objects.get_or_create(user=leave.employee)
    remaining = _remaining_for(balance, leave.leave_type)

    if leave.total_days > remaining:
        messages.error(
            request,
            f"Cannot approve — {leave.employee.full_name} only has {remaining} {leave.leave_type} day(s) left.",
        )
        return redirect("leaves:admin_list")

    _deduct_for(balance, leave.leave_type, leave.total_days)
    balance.save()

    leave.status = "Approved"
    leave.approved_by = request.user
    leave.approved_at = timezone.now()
    leave.save()

    messages.success(request, "Leave approved.")
    return redirect("leaves:admin_list")


@login_required
@user_passes_test(is_admin, login_url="accounts:login")
@require_POST
def reject_leave(request, pk):
    leave = get_object_or_404(LeaveRequest, pk=pk)

    if leave.status != "Pending":
        messages.warning(request, "This request has already been processed.")
        return redirect("leaves:admin_list")

    leave.status = "Rejected"
    leave.approved_by = request.user
    leave.approved_at = timezone.now()
    leave.manager_remark = request.POST.get("remark", "")
    leave.save()

    messages.info(request, "Leave rejected.")
    return redirect("leaves:admin_list")
