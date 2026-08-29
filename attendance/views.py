from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from datetime import datetime

from .models import Attendance, Holiday


def is_admin(user):
    return user.is_authenticated and user.is_admin_role()


def is_employee(user):
    return user.is_authenticated and user.is_employee_role()


@login_required
@user_passes_test(is_employee, login_url="accounts:login")
def my_attendance(request):
    today = timezone.localdate()
    today_record, _ = Attendance.objects.get_or_create(employee=request.user, date=today)
    records = request.user.attendance_records.exclude(pk=today_record.pk)
    return render(request, "attendance/my_attendance.html", {
        "today_record": today_record,
        "records": records,
    })


@login_required
@user_passes_test(is_employee, login_url="accounts:login")
def punch_in(request):
    today = timezone.localdate()
    record, _ = Attendance.objects.get_or_create(employee=request.user, date=today)
    if record.in_time:
        messages.warning(request, "You've already punched in today.")
    else:
        record.in_time = timezone.localtime().time()
        record.status = "Present"
        record.save()
        messages.success(request, "Punched in.")
    return redirect("attendance:my_attendance")


@login_required
@user_passes_test(is_employee, login_url="accounts:login")
def punch_out(request):
    today = timezone.localdate()
    record, _ = Attendance.objects.get_or_create(employee=request.user, date=today)
    if not record.in_time:
        messages.error(request, "Punch in before punching out.")
    elif record.out_time:
        messages.warning(request, "You've already punched out today.")
    else:
        record.out_time = timezone.localtime().time()
        in_dt = datetime.combine(today, record.in_time)
        out_dt = datetime.combine(today, record.out_time)
        hours = (out_dt - in_dt).total_seconds() / 3600
        record.working_hours = round(hours, 2)
        record.save()
        messages.success(request, "Punched out.")
    return redirect("attendance:my_attendance")


@login_required
@user_passes_test(is_admin, login_url="accounts:login")
def attendance_admin_list(request):
    records = Attendance.objects.select_related("employee").order_by("-date")[:200]
    return render(request, "attendance/admin_list.html", {"records": records})


@login_required
def holiday_list(request):
    if request.method == "POST":
        if not request.user.is_admin_role():
            messages.error(request, "Only admins can add holidays.")
            return redirect("attendance:holidays")
        date = request.POST.get("date")
        name = request.POST.get("name")
        if date and name:
            Holiday.objects.get_or_create(date=date, defaults={"name": name})
            messages.success(request, "Holiday added.")
        return redirect("attendance:holidays")

    holidays = Holiday.objects.all()
    return render(request, "attendance/holidays.html", {"holidays": holidays})