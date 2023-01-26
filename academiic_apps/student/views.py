from django.db.models import Q
from django.http import HttpResponse

from academiic_apps.management.models import Level
from academiic_apps.student.forms import StudentsForm
from academiic_apps.student.models import Students
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView, FormView


# Create your views here.


class addStudent(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Students
    form_class = StudentsForm
    success_url = reverse_lazy('view_all_students')
    success_message = "Student added successfully"


class StudentList(LoginRequiredMixin, ListView):
    template_name = "student/students_list.html"
    model = Students

    def get_queryset(self):
        return Students.objects.select_related('level').filter(level__slug__icontains=self.kwargs.get('slug')) \
            .select_related('section').filter(section__section__icontains=self.kwargs.get('section'))


class AllStudentView(LoginRequiredMixin, ListView):
    template_name = "student/students_list.html"
    model = Students

    def get_queryset(self):
        return Students.objects.filter(Q(status="ENROLLED") | Q(status="REPEATER"))


class StudentInactiveView(LoginRequiredMixin, ListView):
    template_name = "student/students_list.html"
    model = Students

    def get_queryset(self):
        return Students.objects.exclude(Q(status="ENROLLED") | Q(status="REPEATER"))


class StudentUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Students
    form_class = StudentsForm
    success_url = reverse_lazy('view_all_students')
    success_message = "Student Details Updated Successfully!"


class StudentDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = "Student.delete_student"
    permission_denied_message = 'You do not have access to this page.'
    success_message = "Student Record Deleted!!"
    model = Students
    fields = [
        "last_Name",
        "first_Name",
        "middle_Name",
        "address",
        "birthdate",
        "admission_Date",
        "gender",
        "level",
        "status"
    ]
    success_url = reverse_lazy('view_all_students')


class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Students


class Student_Grade(LoginRequiredMixin, DetailView):
    model = Students
    template_name = "student/student_grade.html"


def load_students(request):
    section_id = request.GET.get('section')
    students = Students.objects.filter(section_id=section_id).order_by('section')
    return render(request, "student/load_students.html", {'students': students})




