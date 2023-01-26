from django import forms
from django.http import request

from academiic_apps.faculty.models import Faculty


class DateInput(forms.DateInput):
    input_type = 'date'


class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = [
            "address",
            "employment_Date",
        ]
        widgets = {
            'employment_Date': DateInput()
        }

