from academiic_apps.management.models import AcademicYear, Level
from academiic_apps.subjects.models import Subject
from django import forms


class AddSubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = {'name', 'faculty', 'section', 'academic_Year'}

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['section'].widget.attrs.update({'class': 'form-control'})
        self.fields['faculty'].widget.attrs.update({'class': 'form-control'})
        self.fields['academic_Year'] = forms.ModelChoiceField(queryset=AcademicYear.objects.filter(active=True), widget=forms.Select(attrs={'class': 'form-control'}))


class EditSubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = {
            'name',
            'faculty'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['faculty'].widget.attrs.update({'class': 'form-control'})


class SubjectForm(forms.Form):
    year_level = forms.ModelChoiceField(queryset=Level.objects.all(), empty_label="Select Year Level")
    name = forms.CharField(max_length=255)
    academic_Year = forms.HiddenInput()
