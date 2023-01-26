from django.urls import path
from .import views

urlpatterns = [
    path('gradebook/', views.add_gradebook, name='add_gradebook'),
    path('gradebook/<int:id>', views.add_gradebook_for, name='add_gradebook_for'),
    path('view_grades/<int:pk>', views.view_gradebook, name='view_grades'),
    path('view_grades/<int:pk>/year/<int:a_pk>', views.view_gradebook_for, name='view_grades_for'),
]
