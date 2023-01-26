from django.urls import path

from . import views
from .views import addFaculty, facultyList, FacultyDetail, FacultyDelete, Profile


urlpatterns = [
    path('add_faculty', addFaculty.as_view(), name='add_faculty'),
    path('view_faculty', facultyList.as_view(), name='view_faculty'),
    path('view_faculty/<int:pk>', FacultyDetail.as_view(), name='faculty_detail'),
    path('profile/<int:pk>', Profile.as_view(), name='profile'),
    path('profile_edit/<int:pk>', views.update_profile, name='update_profile'),
    path('faculty_delete/<int:pk>', FacultyDelete.as_view(), name='faculty_delete'),
]