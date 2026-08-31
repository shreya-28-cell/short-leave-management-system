from django import forms
from accounts.models import User


class EmployeeCreateForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Temporary password",
        help_text="The employee can log in with this right away.",
    )

    class Meta:
        model = User
        fields = ["full_name", "email", "employee_code", "department", "designation", "mobile", "password"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "employee"
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user