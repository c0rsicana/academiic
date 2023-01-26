from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
from django.utils.text import slugify

from academiic_apps.faculty.models import Faculty


class SiteConfig(models.Model):
    """Site Configurations"""

    key = models.SlugField()
    value = models.CharField(max_length=200)

    def __str__(self):
        return self.key


class MyAccountManager(BaseUserManager):

    def create_user(self, email, password, **other_fields):
        if not email:
            raise ValueError("You must Provide an Email Address")
        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_admin', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_verified', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError("Superuser must be a staff")
        if other_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must be a superuser")

        return self.create_user(email, **other_fields)


class Staff(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    first_name = models.CharField(max_length=32, blank=True, validators=[RegexValidator(r'^[A-Za-z\s]+$',
                                                                                        'First Name must contain only '
                                                                                        'alphabetical characters')])
    last_name = models.CharField(max_length=32, blank=True, validators=[RegexValidator(r'^[A-Za-z\s]+$',
                                                                                        'Last Name must contain only '
                                                                                        'alphabetical characters')])
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_faculty = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = MyAccountManager()

    def get_fullname(self):
        fullname = self.first_name + " " + self.last_name
        return fullname

    def save(self, *args, **kwargs):
        self.slug = slugify(self.get_fullname())
        super(Staff, self).save(*args, **kwargs)

    def __str__(self):
        return format(self.get_fullname())
