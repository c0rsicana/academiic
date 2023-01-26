from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from academiic_apps.faculty.models import Faculty
from academiic_apps.management.models import Section, AcademicYear
from academiic_apps.subjects.models import Subject
from academiic_apps.subjects.forms import AddSubjectForm, EditSubjectForm, SubjectForm
from django.shortcuts import render, redirect, get_object_or_404


# Create your views here.

@login_required
def load_subjects(request):
    level_id = request.GET.get('level')
    subjects = Subject.objects.filter(level_id=level_id).order_by('level')
    return render(request, "subjects/load_subjects.html", {'subjects': subjects})


@user_passes_test(lambda u: u.is_superuser)
def edit_subject(request, pk):
    active_year = AcademicYear.objects.get(active=True)
    faculties = Faculty.objects.all()
    subject = Subject.objects.get(pk=pk)
    section = subject.section
    if request.method == 'POST':
        form = EditSubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, "Subject Updated")
            return redirect('subjects:list_subjects')
        else:
            messages.warning(request, "Something Went Wrong, Please Try Again")
            return redirect('subjects:list_subjects')
    else:
        form = EditSubjectForm(instance=subject)

    if request.user.is_authenticated:
        return render(request, 'subjects/edit_subject.html',
                      {'form': form, 'subject': subject, 'faculties': faculties, 'active_year': active_year})
    else:
        return redirect('login')


@user_passes_test(lambda u: u.is_superuser)
def delete_subject(request, pk):
    subject = Subject.objects.get(pk=pk)
    subject.delete()
    return redirect('subjects:list_subjects')


@login_required
def list_subjects(request):
    active_year = AcademicYear.objects.get(active=True)
    faculty = Faculty.objects.all()
    subjects = Subject.objects.filter(academic_Year=active_year).order_by('-id')

    paginator = Paginator(subjects, 5)  # Show 5 subjects per page
    page = request.GET.get('page')
    subjects = paginator.get_page(page)

    if request.user.is_authenticated:
        return render(request, 'subjects/list_subjects.html', {'subjects': subjects, 'active_year': active_year, 'faculty': faculty})
    else:
        return redirect('login')


class CreateSubjectsView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    permission_required = "Subject.create_subject"
    permission_denied_message = "You do not have access to this page"
    template_name = 'subjects/create_subjects.html'
    form_class = SubjectForm
    success_message = "Subject Added"
    success_url = reverse_lazy('subjects:list_subjects')

    def form_valid(self, form):
        year_level = form.cleaned_data['year_level'].id
        sections = Section.objects.filter(level=year_level)
        academic_Year = AcademicYear.objects.get(active=True)
        name = form.cleaned_data['name']

        for section in sections:
            existing_subject = Subject.objects.filter(section=section, name=name, academic_Year=academic_Year)
            if existing_subject.exists():
                form.add_error(None, "A subject with the same name and section already exists.")
                return self.form_invalid(form)
            Subject.objects.create(section=section, name=name, academic_Year=academic_Year)

        return super().form_valid(form)

