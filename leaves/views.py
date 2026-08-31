from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db.models import Case, When, Value, IntegerField

from accounts.models import User
from .models import LeaveRequest, LeaveBalance, ShortLeaveRequest
from .forms import LeaveApplicationForm, ShortLeaveApplicationForm
from notifications.utils import notify

MAX_SHORT_LEAVES_PER_MONTH = 2


def is_admin(user):
    return user.is_authenticated and user.is_admin_role()


def is_employee(user):
    return user.is_authenticated and user.is_employee_role()


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

            for admin_user in User.objects.filter(role="admin"):
                notify(
                    admin_user,
                    "New leave request",
                    f"{request.user.full_name} applied for {leave.leave_type} "
                    f"({leave.from_date} to {leave.to_date}, {leave.total_days} day(s)).",
                )

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

    notify(
        leave.employee,
        "Leave approved",
        f"Your {leave.leave_type} request ({leave.from_date} to {leave.to_date}) was approved.",
    )

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

    remark_note = f" Remark: {leave.manager_remark}" if leave.manager_remark else ""
    notify(
        leave.employee,
        "Leave rejected",
        f"Your {leave.leave_type} request ({leave.from_date} to {leave.to_date}) was rejected.{remark_note}",
    )

    messages.info(request, "Leave rejected.")
    return redirect("leaves:admin_list")


@login_required
@user_passes_test(is_employee, login_url="accounts:login")
def apply_short_leave(request):
    today = timezone.localdate()
    used_this_month = ShortLeaveRequest.objects.filter(
        employee=request.user,
        date__year=today.year,
        date__month=today.month,
    ).exclude(status="Rejected").count()

    if request.method == "POST":
        if used_this_month >= MAX_SHORT_LEAVES_PER_MONTH:
            messages.error(request, f"You've used your {MAX_SHORT_LEAVES_PER_MONTH} short leaves for this month.")
            return redirect("leaves:my_short_leaves")

        form = ShortLeaveApplicationForm(request.POST)
        if form.is_valid():
            short_leave = form.save(commit=False)
            short_leave.employee = request.user
            short_leave.save()

            for admin_user in User.objects.filter(role="admin"):
                notify(
                    admin_user,
                    "New short leave request",
                    f"{request.user.full_name} requested short leave on {short_leave.date} "
                    f"({short_leave.from_time.strftime('%I:%M %p')} to {short_leave.to_time.strftime('%I:%M %p')}).",
                )

            messages.success(request, "Short leave request submitted.")
            return redirect("leaves:my_short_leaves")
    else:
        form = ShortLeaveApplicationForm()

    remaining = max(MAX_SHORT_LEAVES_PER_MONTH - used_this_month, 0)
    return render(request, "leaves/apply_short_leave.html", {"form": form, "remaining": remaining})


@login_required
@user_passes_test(is_employee, login_url="accounts:login")
def my_short_leaves(request):
    today = timezone.localdate()
    used_this_month = ShortLeaveRequest.objects.filter(
        employee=request.user,
        date__year=today.year,
        date__month=today.month,
    ).exclude(status="Rejected").count()
    remaining = max(MAX_SHORT_LEAVES_PER_MONTH - used_this_month, 0)
    short_leaves = request.user.short_leave_requests.all()
    return render(request, "leaves/my_short_leaves.html", {
        "short_leaves": short_leaves,
        "remaining": remaining,
    })


@login_required
@user_passes_test(is_admin, login_url="accounts:login")
def short_leave_requests_admin(request):
    short_leaves = (
        ShortLeaveRequest.objects.select_related("employee")
        .annotate(
            priority=Case(
                When(status="Pending", then=Value(0)),
                default=Value(1),
                output_field=IntegerField(),
            )
        )
        .order_by("priority", "-applied_at")
    )
    return render(request, "leaves/short_leave_admin_list.html", {"short_leaves": short_leaves})


@login_required
@user_passes_test(is_admin, login_url="accounts:login")
@require_POST
def approve_short_leave(request, pk):
    sl = get_object_or_404(ShortLeaveRequest, pk=pk)
    if sl.status != "Pending":
        messages.warning(request, "This request has already been processed.")
        return redirect("leaves:short_leave_admin_list")

    sl.status = "Approved"
    sl.approved_by = request.user
    sl.approved_at = timezone.now()
    sl.save()

    notify(
        sl.employee,
        "Short leave approved",
        f"Your short leave on {sl.date} ({sl.from_time.strftime('%I:%M %p')}–{sl.to_time.strftime('%I:%M %p')}) was approved.",
    )
    messages.success(request, "Short leave approved.")
    return redirect("leaves:short_leave_admin_list")


@login_required
@user_passes_test(is_admin, login_url="accounts:login")
@require_POST
def reject_short_leave(request, pk):
    sl = get_object_or_404(ShortLeaveRequest, pk=pk)
    if sl.status != "Pending":
        messages.warning(request, "This request has already been processed.")
        return redirect("leaves:short_leave_admin_list")

    sl.status = "Rejected"
    sl.approved_by = request.user
    sl.approved_at = timezone.now()
    sl.manager_remark = request.POST.get("remark", "")
    sl.save()

    remark_note = f" Remark: {sl.manager_remark}" if sl.manager_remark else ""
    notify(sl.employee, "Short leave rejected", f"Your short leave on {sl.date} was rejected.{remark_note}")
    messages.info(request, "Short leave rejected.")
    return redirect("leaves:short_leave_admin_list")