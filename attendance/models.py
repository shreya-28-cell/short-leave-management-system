from django.db import models
from django.utils import timezone
from accounts.models import User


class Attendance(models.Model):
    STATUS_CHOICES = (
        ("Present", "Present"),
        ("Absent", "Absent"),
    )

    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="attendance_records")
    date = models.DateField(default=timezone.localdate)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Present")
    in_time = models.TimeField(null=True, blank=True)
    out_time = models.TimeField(null=True, blank=True)
    working_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        unique_together = ("employee", "date")
        ordering = ["-date"]

    def __str__(self):
        return f"{self.employee.full_name} — {self.date}"


class Holiday(models.Model):
    date = models.DateField(unique=True)
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return f"{self.name} ({self.date})"