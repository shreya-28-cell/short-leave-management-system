from django.db import models
from accounts.models import User


class LeaveBalance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="leave_balance")

    casual_leave = models.DecimalField(max_digits=5, decimal_places=1, default=12)
    sick_leave = models.DecimalField(max_digits=5, decimal_places=1, default=10)
    paid_leave = models.DecimalField(max_digits=5, decimal_places=1, default=15)

    used_casual_leave = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    used_sick_leave = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    used_paid_leave = models.DecimalField(max_digits=5, decimal_places=1, default=0)

    def __str__(self):
        return f"Leave balance — {self.user.full_name}"

    @property
    def remaining_casual(self):
        return self.casual_leave - self.used_casual_leave

    @property
    def remaining_sick(self):
        return self.sick_leave - self.used_sick_leave

    @property
    def remaining_paid(self):
        return self.paid_leave - self.used_paid_leave


class LeaveRequest(models.Model):
    LEAVE_TYPE_CHOICES = (
        ("Casual Leave", "Casual Leave"),
        ("Sick Leave", "Sick Leave"),
        ("Paid Leave", "Paid Leave"),
    )
    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    )

    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="leave_requests")
    leave_type = models.CharField(max_length=30, choices=LEAVE_TYPE_CHOICES)
    from_date = models.DateField()
    to_date = models.DateField()
    total_days = models.DecimalField(max_digits=5, decimal_places=1)
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")

    applied_at = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_leaves"
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    manager_remark = models.CharField(max_length=500, blank=True)

    class Meta:
        ordering = ["-applied_at"]

    def __str__(self):
        return f"{self.employee.full_name} — {self.leave_type} ({self.status})"


class ShortLeaveRequest(models.Model):
   
    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    )

    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="short_leave_requests")
    date = models.DateField()
    from_time = models.TimeField()
    to_time = models.TimeField()
    reason = models.CharField(max_length=500, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")

    applied_at = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_short_leaves"
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    manager_remark = models.CharField(max_length=500, blank=True)

    class Meta:
        ordering = ["-applied_at"]

    def __str__(self):
        return f"{self.employee.full_name} — Short Leave {self.date} ({self.from_time}–{self.to_time})"

    @property
    def duration_hours(self):
        from datetime import datetime
        start = datetime.combine(self.date, self.from_time)
        end = datetime.combine(self.date, self.to_time)
        return round((end - start).total_seconds() / 3600, 2)