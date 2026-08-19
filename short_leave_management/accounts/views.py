from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render


class UserLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')