from django import forms
from .models import LeaveRequest, ShortLeaveRequest


class LeaveApplicationForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ["leave_type", "from_date", "to_date", "reason"]
        widgets = {
            "from_date": forms.DateInput(attrs={"type": "date"}),
            "to_date": forms.DateInput(attrs={"type": "date"}),
            "reason": forms.Textarea(attrs={"rows": 4}),
        }

    def clean(self):
        cleaned_data = super().clean()
        from_date = cleaned_data.get("from_date")
        to_date = cleaned_data.get("to_date")
        if from_date and to_date and to_date < from_date:
            raise forms.ValidationError("End date can't be before the start date.")
        return cleaned_data


class ShortLeaveApplicationForm(forms.ModelForm):
    class Meta:
        model = ShortLeaveRequest
        fields = ["date", "from_time", "to_time", "reason"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "from_time": forms.TimeInput(attrs={"type": "time"}),
            "to_time": forms.TimeInput(attrs={"type": "time"}),
            "reason": forms.Textarea(attrs={"rows": 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        from_time = cleaned_data.get("from_time")
        to_time = cleaned_data.get("to_time")
        if from_time and to_time and to_time <= from_time:
            raise forms.ValidationError("End time must be after the start time.")
        return cleaned_data