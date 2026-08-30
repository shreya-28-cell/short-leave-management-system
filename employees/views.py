from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from accounts.models import User
from .forms import EmployeeCreateForm


def is_admin(user):
    return user.is_authenticated and user.is_admin_role()


@login_required
@user_passes_test(is_admin, login_url="accounts:login")
def employee_list(request):
    employees = User.objects.filter(role="employee").order_by("full_name")
    return render(request, "employees/list.html", {"employees": employees})


@login_required
@user_passes_test(is_admin, login_url="accounts:login")
def employee_add(request):
    if request.method == "POST":
        form = EmployeeCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee added successfully.")
            return redirect("employees:list")
    else:
        form = EmployeeCreateForm()
    return render(request, "employees/add.html", {"form": form})


@login_required
@user_passes_test(is_admin, login_url="accounts:login")
@require_POST
def employee_toggle_active(request, pk):
    employee = get_object_or_404(User, pk=pk, role="employee")
    employee.is_active_employee = not employee.is_active_employee
    employee.is_active = employee.is_active_employee  # this actually blocks/allows login
    employee.save()
    state = "activated" if employee.is_active_employee else "deactivated"
    messages.success(request, f"{employee.full_name} was {state}.")
    return redirect("employees:list")


@login_required
@user_passes_test(is_admin, login_url="accounts:login")
@require_POST
def employee_delete(request, pk):
    employee = get_object_or_404(User, pk=pk, role="employee")
    name = employee.full_name
    employee.delete()
    messages.success(request, f"{name} was permanently deleted, along with their leave, attendance, and notification history.")
    return redirect("employees:list")


@login_required
def my_profile(request):
    return render(request, "employees/profile.html", {"profile_user": request.user})