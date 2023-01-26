from django.db import models
from django.urls import reverse

from academiic_apps.grading.models import Gradebook
from academiic_apps.management.models import Level, Section, AcademicYear
from django.core.validators import MinLengthValidator, RegexValidator
from django.utils.text import slugify
# Create your models here.


class Students(models.Model):
    LRN = models.CharField(max_length=12, unique=True,
                           validators=[RegexValidator(r'^\d{12}$', 'LRN must be a 12 digit number')])
    first_Name = models.CharField(max_length=50,
                                  validators=[RegexValidator(r'^[A-Za-z\s]+$',
                                                             'First Name must contain only alphabetical characters')])
    middle_Name = models.CharField(max_length=50,
                                   validators=[RegexValidator(r'^[A-Za-z\s]+$',
                                                              'Middle Name must contain only alphabetical characters')])
    last_Name = models.CharField(max_length=50,
                                 validators=[RegexValidator(r'^[A-Za-z\s]+$',
                                                            'Last Name must contain only alphabetical characters')])
    suffix_Name = models.CharField(max_length=50, blank=True, null=True, default='', validators=[
        RegexValidator(r'^[A-Za-z\s]+$', 'Suffix Name must contain only alphabetical characters')])
    address = models.CharField(max_length=255)
    birthdate = models.DateField(null=True)
    admission_Date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    GENDER = (
        (MALE, 'MALE'),
        (FEMALE, 'FEMALE')
    )
    gender = models.CharField(choices=GENDER, max_length=10)
    ENROLLED = 'ENROLLED'
    TRANSFERRED = 'TRANSFERRED'
    GRADUATED = 'GRADUATED'
    REPEATER = 'REPEATER'
    LEAVER = 'LEAVER'
    DROPPED = 'DROPPED'
    STATUS = (
        (ENROLLED, 'ENROLLED'),
        (TRANSFERRED, 'TRANSFERRED'),
        (GRADUATED, 'GRADUATED'),
        (LEAVER, 'LEAVER'),
        (DROPPED, 'DROPPED')
    )
    status = models.CharField(choices=STATUS, max_length=15, default=ENROLLED)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)




    def save(self, *args, **kwargs):
        self.slug = slugify(self.LRN)
        super(Students, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('student_grade', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['level']
        unique_together = ['first_Name', 'last_Name']

    def __str__(self):
        return format(self.first_Name + " " + self.middle_Name + " " + self.last_Name)


