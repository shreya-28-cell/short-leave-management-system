from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


class RoleBasedLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.is_admin_role():
            return reverse_lazy("dashboard:admin_dashboard")
        return reverse_lazy("dashboard:employee_dashboard")
