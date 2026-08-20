from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from employees.models import EmployeeProfile


class EmployeeRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    employee_id = forms.CharField(max_length=20)
    department = forms.CharField(max_length=100)
    designation = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "employee_id",
            "department",
            "designation",
            "password1",
            "password2",
        ]

    def clean_employee_id(self):
        employee_id = self.cleaned_data["employee_id"]

        if EmployeeProfile.objects.filter(employee_id=employee_id).exists():
            raise forms.ValidationError("This Employee ID already exists.")

        return employee_id