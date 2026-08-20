from django import forms

from .models import ShortLeave


class ShortLeaveForm(forms.ModelForm):
    class Meta:
        model = ShortLeave
        fields = ["leave_date", "start_time", "end_time", "reason"]
        widgets = {
            "leave_date": forms.DateInput(attrs={"type": "date"}),
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "end_time": forms.TimeInput(attrs={"type": "time"}),
            "reason": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Why do you need short leave?"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if start_time and end_time and end_time <= start_time:
            raise forms.ValidationError(
                "End time must be later than start time."
            )

        return cleaned_data