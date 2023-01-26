from academiic_apps.grading.models import Gradebook
from academiic_apps.management.models import Section
from academiic_apps.student.models import Students
from django import forms
from django.forms import TextInput
from django.forms.models import inlineformset_factory
from django.utils.safestring import mark_safe


class DateInput(forms.DateInput):
    input_type = 'date'


class StudentsForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = [
            "LRN",
            "last_Name",
            "first_Name",
            "middle_Name",
            "suffix_Name",
            "address",
            "birthdate",
            "admission_Date",
            "section",
            "level",
            "gender",
            "status",
        ]
        widgets = {
            'birthdate': DateInput(),
            'admission_Date': DateInput(),
            'suffix_Name': TextInput(attrs={'placeholder': 'Optional'}),
            'LRN': TextInput(attrs={'placeholder': '12 Digit Learner Reference Number'}),
        }
        help_texts = {
            'section': mark_safe('Click <a href="/management/add_section">here</a> to add new Section'),
            'academic_Year_of_Admission': mark_safe('Click <a href="/management/add_academic_year">here</a> to add an Academic Year'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['section'].queryset = Section.objects.none()

        if 'level' in self.data:
            try:
                level_id = int(self.data.get('level'))
                self.fields['section'].queryset = Section.objects.filter(level_id=level_id).order_by('level')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['section'].queryset = self.instance.level.section_set.order_by('level')

