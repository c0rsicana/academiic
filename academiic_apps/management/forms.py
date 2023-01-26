from academiic_apps.management.models import AcademicYear, Quarter, Section, Level
from academiic_apps.subjects.models import Subject
from academiic_apps.faculty.models import Faculty
from academiic_apps.core.models import Staff
from django import forms
from django.forms.models import inlineformset_factory
from django.utils.safestring import mark_safe


class CurrentYearForm(forms.Form):
    active_year = forms.ModelChoiceField(
        queryset=AcademicYear.objects.all(),
        help_text=mark_safe(
            'Click <a href="add_academic_year">here</a> to add new academic year')
    )
    active_quarter = forms.ModelChoiceField(
        queryset=Quarter.objects.all(),
        help_text=mark_safe(
            'Click <a href="add_quarter">here</a> to add new quarter')
    )


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = [
            "level", "section"
        ]


SubjectFormset = inlineformset_factory(Section, Subject, fields=('name', 'faculty'), extra=1)




