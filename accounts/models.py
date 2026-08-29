from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import UserManager


class User(AbstractUser):
    username = None

    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("employee", "Employee"),
    )

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="employee")

    employee_code = models.CharField(max_length=20, blank=True, null=True, unique=True)
    department = models.CharField(max_length=50, blank=True, null=True)
    designation = models.CharField(max_length=50, blank=True, null=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    is_active_employee = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    objects = UserManager()

    def __str__(self):
        return f"{self.full_name} ({self.role})"

    def is_admin_role(self):
        return self.role == "admin"

    def is_employee_role(self):
        return self.role == "employee"
