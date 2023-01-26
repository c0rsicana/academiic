from django import forms, views
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from academiic_apps.grading.models import Gradebook
from academiic_apps.management.models import Section, AcademicYear, Quarter, Level
from academiic_apps.student.models import Students
from academiic_apps.subjects.models import Subject


# Create your views here.

@login_required
def add_gradebook(request):
    current_year = AcademicYear.objects.get(active=True)
    subjects = Subject.objects.filter(faculty_id=request.user.id).filter(academic_Year=current_year)
    context = {
        "subjects": subjects,
    }
    return render(request, 'grading/add_gradebook.html', context)


@login_required
def add_gradebook_for(request, id):
    current_year = AcademicYear.objects.get(active=True)
    if request.method == 'GET':
        subjects = Subject.objects.filter(faculty_id=request.user.id).filter(academic_Year=current_year)
        subject = Subject.objects.get(pk=id)
        students = Students.objects.filter(section__subject_section__in=[subject])
        grades = Gradebook.objects.filter(subject_id=subject).filter(academic_year_id=current_year)
        context = {
            "subjects": subjects,
            "subject": subject,
            "students": students,
            "grades": grades,
        }
        return render(request, 'grading/add_gradebook_for.html', context)

    if request.method == 'POST':
        ids = ()
        data = request.POST.copy()
        data.pop('csrfmiddlewaretoken', None)
        subject = Subject.objects.get(pk=id)
        for key in data.keys():
            ids = ids + (str(key),)  # gather all the students id in a tuple\
        for s in range(0, len(ids)):
            student = Students.objects.get(id=ids[s])
            score = data.getlist(ids[s]) # get list of score for current student in the loop
            q1 = score[0]
            q2 = score[1]
            q3 = score[2]
            q4 = score[3]
            if float(q1) < 0 or float(q1) > 100 or float(q2) < 0 or float(q2) > 100 or float(q3) < 0 or float(
                    q3) > 100 or float(q4) < 0 or float(q4) > 100:
                messages.warning(request, "Grades should be in value between 0-100")
                return HttpResponseRedirect(reverse_lazy('add_gradebook_for', kwargs={'id': id}))
            Gradebook.objects.update_or_create(student=student, subject=subject, academic_year=current_year,
                                               defaults={'q1_grade': q1, 'q2_grade': q2, 'q3_grade': q3, 'q4_grade': q4})
        messages.success(request, "Grades Successfully Recorded!")
        return HttpResponseRedirect(reverse_lazy('add_gradebook_for', kwargs={'id': id}))



@login_required()
def view_gradebook(request, pk):
    student = Gradebook.objects.filter(student_id=pk)
    student_details = Students.objects.get(pk=pk)
    years = AcademicYear.objects.all()

    context = {
        "student": student,
        "student_details": student_details,
        "years": years,
    }
    return render(request, "grading/view_gradebook.html", context)


@login_required()
def view_gradebook_for(request, pk, a_pk):
    student = Gradebook.objects.filter(student_id=pk)
    student_details = Students.objects.get(pk=pk)
    years = AcademicYear.objects.all()
    year = AcademicYear.objects.get(pk=a_pk)
    grades = Gradebook.objects.filter(academic_year=year).filter(student_id=student_details)

    context = {
        "student": student,
        "years": years,
        "grades": grades,
        "student_details": student_details,
        "year": year,
    }
    return render(request, "grading/view_gradebook_for.html", context)