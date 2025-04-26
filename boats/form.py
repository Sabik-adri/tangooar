from datetime import datetime
import re
from django import forms
from .models import Boat

class BoatForm(forms.ModelForm):
    class Meta:
        model = Boat
        fields = ['owner_profile', 'name', 'description', 'price', 'type', 'cabin_quantity', 'length', 'width', 'height', 'booked_dates', 'photos']
        widgets = {
            'booked_dates': forms.TextInput(attrs={'id': 'booked_dates'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_booked_dates(self):
        booked_dates = self.cleaned_data.get('booked_dates')
        if booked_dates:
            date_ranges = booked_dates.split(",")
            date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}:\d{4}-\d{2}-\d{2}$")
            for date_range in date_ranges:
                if not date_range.strip() or not date_pattern.match(date_range):
                    raise forms.ValidationError(f"Invalid date range format: {date_range}")
                start_date, end_date = date_range.split(":")
                start = datetime.strptime(start_date, "%Y-%m-%d")
                end = datetime.strptime(end_date, "%Y-%m-%d")
                if start > end:
                    raise forms.ValidationError(f"Start date must be before end date in range: {date_range}")
        return booked_dates