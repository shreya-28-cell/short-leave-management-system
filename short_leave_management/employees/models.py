from django.contrib.auth.models import User
from django.db import models


class EmployeeProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100, blank=True)
    designation = models.CharField(max_length=100, blank=True)
    joining_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.employee_id} - {self.user.username}"