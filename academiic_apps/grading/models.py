from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse

from academiic.settings import AUTH_USER_MODEL
from academiic_apps.management.models import Level, Section, AcademicYear, Quarter
from academiic_apps.subjects.models import Subject

from django.utils import timezone
# Create your models here.


class Gradebook(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    student = models.ForeignKey('student.Students', on_delete=models.CASCADE, related_name='student_grade')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    q1_grade = models.DecimalField(
        decimal_places=2, max_digits=5,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True, blank=True
    )
    q2_grade = models.DecimalField(
        decimal_places=2, max_digits=5,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True, blank=True
    )
    q3_grade = models.DecimalField(
        decimal_places=2, max_digits=5,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True, blank=True
    )
    q4_grade = models.DecimalField(
        decimal_places=2, max_digits=5,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True, blank=True
    )

    def average_grade(self):
        return (self.q1_grade + self.q2_grade + self.q3_grade + self.q4_grade) / 4

    def student_average_grade(self):
        student_grades = Gradebook.objects.filter(student=self.student)
        subject_averages = [grade.average_grade() for grade in student_grades]
        return sum(subject_averages) / len(subject_averages)

    class Meta:
        ordering = ["student"]

    def save(self, *args, **kwargs):
        super(Gradebook, self).save(*args, **kwargs)
        self.student.save()
