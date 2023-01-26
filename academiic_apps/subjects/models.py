from django.db import models
from django.urls import reverse

from academiic.settings import AUTH_USER_MODEL
from academiic_apps.management.models import Level, Section, AcademicYear


# Create your models here.


class Subject(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="subject_section", null=True)
    name = models.CharField(max_length=255)
    faculty = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    academic_Year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ["section"]
        unique_together = ["section", "name", "academic_Year"]

    def get_absolute_url(self):
        return reverse('subject_detail', kwargs={'id': self.id})

    def __str__(self):
        return format(self.name)
