from academiic.settings import AUTH_USER_MODEL
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.text import slugify
# Create your models here.


class Faculty(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, unique=True)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    employment_Date = models.DateField(null=True)


    def __str__(self):
        return format(self.user)
