from datetime import datetime

from academiic_apps.core.forms import SiteConfigForm, RegistrationForm
from academiic_apps.core.models import SiteConfig, Staff
from academiic_apps.management.models import Level, Announcement
from academiic_apps.student.models import Students
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
# Create your views here.
from academiic_apps.faculty.models import Faculty
from academiic_apps.subjects.models import Subject


class SiteConfigView(LoginRequiredMixin, View):
    """Site Config View"""

    form_class = SiteConfigForm
    template_name = "core/siteconfig.html"

    def get(self, request, *args, **kwargs):
        formset = self.form_class(queryset=SiteConfig.objects.all())
        context = {"formset": formset}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        formset = self.form_class(request.POST)
        if formset.is_valid():
            formset.save()
            messages.success(request, "Configurations successfully updated")
        context = {"formset": formset, "title": "Configuration"}
        return render(request, self.template_name, context)


@login_required()
def showHomepage(request):
    user = request.user
    staffs = Faculty.objects.all().order_by("?")
    students = Students.objects.all().order_by("?")
    classes = Subject.objects.filter(faculty_id=user).order_by("?")
    now = datetime.now()
    announcements = Announcement.objects.filter(date_expired__gte=now).order_by('-created_at')[:5]
    return render(request, "home.html", context={"staffs": staffs, "students": students, "classes": classes, "announcements": announcements})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_verified:
                    login(request, user)
                    messages.info(request, f"Login Success")
                    return redirect("home")
                else:
                    messages.warning(request, "User needs to be approved by admin.")
            else:
                messages.warning(request, "Invalid username or password.")
        else:
            messages.warning(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, "core/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have logged out.")
    return redirect("home")


def registration_view(request):
    context = {}
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, f"Account Created, awaiting admin confirmation")
            return redirect("login")
        else:
            # Add an error message if the form is invalid
            messages.warning(request, "There was an error with your submission. Please try again.")
    else:
        form = RegistrationForm()
    context['registration_form'] = form
    return render(request, 'core/signup.html', context)
