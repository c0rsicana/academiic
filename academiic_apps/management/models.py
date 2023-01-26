from datetime import datetime, timedelta
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
# Create your models here.


class AcademicYear(models.Model):
    """"Academic Year"""
    academic_Year = models.CharField(max_length=10, unique=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['academic_Year']

    def __str__(self):
        return format(self.academic_Year)

class Quarter(models.Model):
    QUARTER1 = "1ST QUARTER"
    QUARTER2 = "2ND QUARTER"
    QUARTER3 = "3RD QUARTER"
    QUARTER4 = "4TH QUARTER"
    QUARTER = (
        (QUARTER1, '1ST QUARTER'),
        (QUARTER2, '2ND QUARTER'),
        (QUARTER3, '3RD QUARTER'),
        (QUARTER4, '4TH QUARTER')
    )
    quarter = models.CharField(choices=QUARTER, max_length=15, default=QUARTER1, unique=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['quarter']

    def __str__(self):
        return format(self.quarter)


class Level(models.Model):
    GRADE7 = 'GRADE 7'
    GRADE8 = 'GRADE 8'
    GRADE9 = 'GRADE 9'
    GRADE10 = 'GRADE 10'
    JUNIOR = 'JUNIOR'
    SENIOR = 'SENIOR'
    LEVEL = (
        (GRADE7, 'GRADE 7'),
        (GRADE8, 'GRADE 8'),
        (GRADE9, 'GRADE 9'),
        (GRADE10, 'GRADE 10'),
        (JUNIOR, 'JUNIOR'),
        (SENIOR, 'SENIOR')
    )
    level = models.CharField(choices=LEVEL, max_length=15, default=GRADE7, unique=True)
    slug = models.SlugField(unique=True, null=True)

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.level)
        super().save(self, *args, **kwargs)

    def get_absolute_url(self):
        return reverse('level_detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return format(self.level)


class Section(models.Model):
    level = models.ForeignKey(Level, null=True, on_delete=models.CASCADE)
    section = models.CharField(max_length=15)

    class Meta:
        ordering = ["level"]
        unique_together = [["level", "section"]]

    def get_absolute_url(self):
        return reverse('section_detail', kwargs={'slug': self.level.slug, 'pk': self.pk})

    def __str__(self):
        return format(self.section)


class Announcement(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField()
    date_expired = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = datetime.now()
            self.date_expired = self.created_at + timedelta(days=30)
        super(Announcement, self).save(*args, **kwargs)
