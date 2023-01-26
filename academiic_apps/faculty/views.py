from django.contrib import messages
from django.shortcuts import redirect, render

from academiic_apps.core.models import Staff
from academiic_apps.faculty.forms import FacultyForm
from academiic_apps.faculty.models import Faculty
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView


# Create your views here.


class addFaculty(SuccessMessageMixin, CreateView):
    permission_required = "Faculty.add_faculty"
    permission_denied_message = 'You do not have access to this page'
    model = Faculty
    form_class = FacultyForm
    success_url = reverse_lazy('view_faculty')
    success_message = "Faculty added successfully"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class facultyList(LoginRequiredMixin, ListView):
    model = Faculty


def update_profile(request, pk):
    profile = Faculty.objects.get(pk=pk)
    if request.method == 'POST':
        form = FacultyForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile Information Updated")
        return redirect('profile', pk=pk)
    else:
        form = FacultyForm(instance=profile)

    if request.user.is_authenticated:
        return render(request, 'faculty/update_profile.html', {'form': form})
    else:
        return redirect('login')


class FacultyDetail(LoginRequiredMixin, DetailView):
    model = Faculty
    template_name = "faculty/faculty_detail.html"

class Profile(LoginRequiredMixin, DetailView):
    model = Faculty
    template_name = "faculty/profile.html"


class FacultyDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = "Faculty.delete_faculty"
    permission_denied_message = 'You do not have access to this page.'
    success_message = "Faculty Record Deleted!"
    model = Faculty
    fields = [
        "full_name"
        "username",
        "password",
        "address",
        "salary_Grade",
        "employment_Date",
    ]
    success_url = reverse_lazy("view_faculty")



