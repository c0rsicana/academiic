from django.contrib.auth.decorators import user_passes_test
from academiic_apps.core.models import Staff
from academiic_apps.faculty.models import Faculty
from academiic_apps.management.forms import SectionForm, CurrentYearForm
from academiic_apps.management.models import AcademicYear, Quarter, Section, Level, Announcement
from academiic_apps.student.models import Students
from academiic_apps.subjects.models import Subject
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.shortcuts import render, redirect
# Create your views here.

class addAcademicYear(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = AcademicYear
    fields = [
        "academic_Year",
    ]
    success_message = "Academic Year added Successfully"
    success_url = reverse_lazy('active_year')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add new session"
        return context


class ListAcademicYear(LoginRequiredMixin, ListView):
    model = AcademicYear


class UpdateAcademicYear(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AcademicYear
    fields = [
        "academic_Year",
    ]
    success_message = "Academic Year Updated Successfully"
    success_url = reverse_lazy('active_year')

    def form_valid(self, form):
        obj = self.object
        if not obj.active:
            terms = (
                AcademicYear.objects.filter(active=True)
                .exclude(academic_Year=obj.academic_Year)
                .exists()
            )
            if not terms:
                messages.warning(self.request, "You must set an Academic Year to current.")
                return redirect("list_academic_year")
        return super().form_valid(form)


class DeleteAcademicYear(LoginRequiredMixin, DeleteView):
    model = AcademicYear
    fields = "__all__"
    success_url = reverse_lazy('list_academic_year')
    success_message = "Academic Year Deleted"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.active:
            messages.warning(request, "Cannot delete Year as it is set to active")
            return redirect("list_academic_year")
        messages.success(self.request, self.success_message.format(obj.academic_Year))
        return super(DeleteAcademicYear, self).delete(request, *args, **kwargs)


class AddQuarter(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Quarter
    fields = [
        "quarter"
    ]
    success_message = "Academic Year added Successfully"
    success_url = reverse_lazy('active_year')


class ListQuarter(LoginRequiredMixin, ListView):
    model = Quarter


class UpdateQuarter(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Quarter
    fields = [
        "quarter",
    ]
    success_message = "Academic Quarter Updated Successfully"
    success_url = reverse_lazy('list_quarter')

    def form_valid(self, form):
        obj = self.object
        if not obj.active:
            terms = (
                Quarter.objects.filter(active=True)
                .exclude(quarter=obj.quarter)
                .exists()
            )
            if not terms:
                messages.warning(self.request, "You must set a Quarter to current.")
                return redirect("add_quarter")
        return super().form_valid(form)


class DeleteQuarter(LoginRequiredMixin, DeleteView):
    model = Quarter
    fields = "__all__"
    success_url = reverse_lazy('list_quarter')
    success_message = "The Quarter has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.active:
            messages.warning(request, "Cannot delete Quarter as it is set to active")
            return redirect("terms")
        messages.success(self.request, self.success_message.format(obj.quarter))
        return super(DeleteQuarter, self).delete(request, *args, **kwargs)


class CurrentYearAndQuarter(LoginRequiredMixin, ListView):
    form_class = CurrentYearForm
    template_name = "management/current-year.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(
            initial={
                "active_year": AcademicYear.objects.get(active=True),
                "active_quarter": Quarter.objects.get(active=True),
            }
        )
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            year = form.cleaned_data["active_year"]
            quarter = form.cleaned_data["active_quarter"]
            AcademicYear.objects.filter(academic_Year=year).update(active=True)
            AcademicYear.objects.exclude(academic_Year=year).update(active=False)
            Quarter.objects.filter(quarter=quarter).update(active=True)
            Quarter.objects.exclude(quarter=quarter).update(active=False)

        return render(request, self.template_name, {"form": form})


def levels_view(request):
    levels = Level.objects.all()

    if request.user.is_authenticated:
        return render(request, "management/levels_list.html", {"levels": levels})
    else:
        return redirect('login')


def levels_detail(request, slug):
    level = Level.objects.get(slug=slug)
    sections = Section.objects.filter(level_id=level)

    if request.user.is_authenticated:
        return render(request, "management/level_detail.html", {"level": level, "sections": sections})
    else:
        return redirect('login')


def sections_detail(request, pk):
    current_year = AcademicYear.objects.get(active=True)
    section = Section.objects.get(pk=pk)
    subjects = Subject.objects.filter(section_id=section).filter(academic_Year=current_year)
    faculty = Faculty.objects.all()

    if request.user.is_authenticated:
        return render(request, "management/section_detail.html", {"section": section, "subjects": subjects, "faculty": faculty})
    else:
        return redirect('login')


class addSection(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Section
    form_class = SectionForm
    success_message = "Section Added successfully"
    success_url = reverse_lazy("list_levels")


class UpdateSection(LoginRequiredMixin, UpdateView):
    model = Section
    fields = [
        "section"
    ]
    success_message = "Section Name Updated Successfully"
    success_url = reverse_lazy('list_section')


class DeleteSection(LoginRequiredMixin, DeleteView):
    model = Section
    fields = "__all__"
    success_url = reverse_lazy('list_section')
    success_message = "The section has been deleted."


def load_sections(request):
    level_id = request.GET.get('level')
    sections = Section.objects.filter(level_id=level_id).order_by('level')
    return render(request, "management/load_sections.html", {'sections': sections})


@user_passes_test(lambda u: u.is_superuser)
def approve_accounts(request):
    unverified_users = Staff.objects.filter(is_verified=False)

    if request.method == 'POST':
        user_ids = request.POST.getlist('user_ids')

        for user_id in user_ids:
            user = Staff.objects.get(pk=user_id)
            user.is_verified = True
            user.save()
            messages.success(request, "Selected Accounts Approved")

    return render(request, 'management/approve_accounts.html', {'unverified_users':unverified_users})


@user_passes_test(lambda u: u.is_superuser)
def create_announcement(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        Announcement.objects.create(title=title, content=content)
        messages.success(request, 'Announcement created successfully')
        return redirect('home')
    return render(request, 'management/create_announcement.html')


@user_passes_test(lambda u: u.is_superuser)
def update_announcement(request, pk):
    announcement = Announcement.objects.get(pk=pk)
    if request.method == 'POST':
        announcement.title = request.POST['title']
        announcement.content = request.POST['content']
        announcement.save()
        messages.success(request, 'Announcement updated successfully')
        return redirect('home')
    return render(request, 'management/update_announcement.html', {'announcement': announcement})


@user_passes_test(lambda u: u.is_superuser)
def delete_announcement(request, pk):
    Announcement.objects.get(pk=pk).delete()
    messages.success(request, 'Announcement deleted successfully')
    return redirect('home')

