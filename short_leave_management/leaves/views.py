from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ShortLeaveForm
from .models import ShortLeave


@login_required
def apply_short_leave(request):
    if request.method == "POST":
        form = ShortLeaveForm(request.POST)

        if form.is_valid():
            short_leave = form.save(commit=False)
            short_leave.employee = request.user
            short_leave.save()

            messages.success(request, "Your short leave request was submitted.")
            return redirect("my_leaves")
    else:
        form = ShortLeaveForm()

    return render(request, "leaves/apply.html", {"form": form})


@login_required
def my_leaves(request):
    leaves = ShortLeave.objects.filter(employee=request.user)

    return render(request, "leaves/my_leaves.html", {"leaves": leaves})