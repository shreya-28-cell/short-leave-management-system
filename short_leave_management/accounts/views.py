from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render

from employees.models import EmployeeProfile

from .forms import EmployeeRegistrationForm


class UserLoginView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True


@login_required
def dashboard(request):
    return render(request, "dashboard.html")


def register(request):
    if request.method == "POST":
        form = EmployeeRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()

            EmployeeProfile.objects.create(
                user=user,
                employee_id=form.cleaned_data["employee_id"],
                department=form.cleaned_data["department"],
                designation=form.cleaned_data["designation"],
            )

            login(request, user)
            messages.success(request, "Registration completed successfully.")
            return redirect("dashboard")
    else:
        form = EmployeeRegistrationForm()

    return render(request, "registration/register.html", {"form": form})