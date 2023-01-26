from django import forms


from academiic_apps.grading.models import Gradebook
from academiic_apps.student.models import Students
from academiic_apps.subjects.models import Subject


class GradeStudentsForm(forms.ModelForm):
    class Meta:
        model = Gradebook
        fields = ('student', 'total_grade',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].queryset = Students.objects.filter(section_id=7)


class GradeTest(forms.Form):
    student = forms.ModelChoiceField(label='student', queryset=Students.objects.all())
    subject = forms.ModelChoiceField(label='subject', queryset=Subject.objects.all())
    total_grade = forms.FloatField(label='Total Grade')




