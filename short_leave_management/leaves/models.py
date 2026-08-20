from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


class ShortLeave(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"

    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="short_leaves"
    )
    leave_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    reason = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )
    applied_at = models.DateTimeField(auto_now_add=True)
    admin_comment = models.TextField(blank=True)

    class Meta:
        ordering = ["-leave_date", "-applied_at"]

    @property
    def duration_hours(self):
        start = datetime.combine(self.leave_date, self.start_time)
        end = datetime.combine(self.leave_date, self.end_time)
        hours = (end - start).total_seconds() / 3600
        return f"{hours:g} hour(s)"

    def __str__(self):
        return f"{self.employee.username} - {self.leave_date}"