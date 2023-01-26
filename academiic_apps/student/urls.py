from django.urls import path
from .views import addStudent, StudentList, AllStudentView, StudentInactiveView, StudentUpdate, StudentDetailView, \
    StudentDelete, load_students


urlpatterns = [
    path('add_student', addStudent.as_view(), name='add_student'),
    path('view_students/<slug:slug>/<str:section>/', StudentList.as_view(), name='view_students'),
    path('view_all_students', AllStudentView.as_view(), name='view_all_students'),
    path('view_inactive', StudentInactiveView.as_view(), name='view_inactive'),
    path('update_student/<slug:slug>', StudentUpdate.as_view(), name='student_update'),
    path('view_student/<slug:slug>', StudentDetailView.as_view(), name='student_detail'),
    path('delete_student/<slug:slug>', StudentDelete.as_view(), name='student_delete'),
    path('ajax/load-students/', load_students, name='ajax_load_students'),
]
