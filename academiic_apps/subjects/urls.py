from django.urls import path

from . import views
from .views import load_subjects, CreateSubjectsView

app_name = 'subjects'

urlpatterns = [
    path('ajax/load-subjects/', load_subjects, name='ajax_load_subjects'),
    path('sections/<int:pk>/edit_subject', views.edit_subject, name='edit_subject'),
    path('sections/<int:pk>/delete_subject/', views.delete_subject, name='delete_subject'),
    path('subjects/all', views.list_subjects, name='list_subjects'),
    path('create_subject', CreateSubjectsView.as_view(), name='create_subjects'),
]
