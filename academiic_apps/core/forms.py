from academiic_apps.core.models import SiteConfig, Staff
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import modelformset_factory


SiteConfigForm = modelformset_factory(
    SiteConfig,
    fields=(
        "key",
        "value",
    ),
    extra=0,
)


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60)

    class Meta:
        model = Staff
        fields = ("email", "first_name", "last_name", "password1", "password2")

