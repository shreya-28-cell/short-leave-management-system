from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from employees.models import EmployeeProfile


class EmployeeRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    employee_id = forms.CharField(max_length=20)

    DEPARTMENT_CHOICES = [
    
    ("", "Select Department"),
    ("CSE", "Computer Science and Engineering"),
    ("IT", "Information Technology"),
    ("ECE", "Electronics and Communication Engineering"),
    ("EEE", "Electrical and Electronics Engineering"),
    ("MECH", "Mechanical Engineering"),
    ("CIVIL", "Civil Engineering"),
    ("AI_DS", "Artificial Intelligence and Data Science"),
    ("AI_ML", "Artificial Intelligence and Machine Learning"),
    ("BCA", "Bachelor of Computer Applications"),
    ("MCA", "Master of Computer Applications"),
    ("BBA", "Bachelor of Business Administration"),
    ("MBA", "Master of Business Administration"),
    ("B.COM", "Bachelor of Commerce"),
    ("OTHER", "Other"),
 
    ]

    department = forms.ChoiceField(
        choices=DEPARTMENT_CHOICES,
        required=True
    )

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