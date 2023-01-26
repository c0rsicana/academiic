from django.urls import path
from . import views
from .views import addAcademicYear, ListAcademicYear, UpdateAcademicYear, DeleteAcademicYear,  \
     AddQuarter, ListQuarter, UpdateQuarter, DeleteQuarter, CurrentYearAndQuarter, addSection, UpdateSection, DeleteSection, load_sections
urlpatterns = [
    path('add_academic_year', addAcademicYear.as_view(), name='add_academic_year'),
    path('list_academic_year', ListAcademicYear.as_view(), name='list_academic_year'),
    path('academic_year_update/<int:pk>', UpdateAcademicYear.as_view(), name='academic_year_update'),
    path('academic_year_delete/<int:pk>', DeleteAcademicYear.as_view(), name='academic_year_delete'),
    path('add_quarter', AddQuarter.as_view(), name='add_quarter'),
    path('list_quarter', ListQuarter.as_view(), name='list_quarter'),
    path('list_quarter', ListQuarter.as_view(), name='list_quarter'),
    path('quarter_update/<int:pk>', UpdateQuarter.as_view(), name='quarter_update'),
    path('quarter_delete/<int:pk>', DeleteQuarter.as_view(), name='quarter_delete'),
    path('active_year', CurrentYearAndQuarter.as_view(), name='active_year'),
    path('list_levels', views.levels_view, name='list_levels'),
    path('level/<slug:slug>/sections', views.levels_detail, name='level_detail'),
    path('sections/<int:pk>', views.sections_detail, name='section_detail'),
    path('add_section', addSection.as_view(), name='add_section'),
    path('section_update/<int:pk>', UpdateSection.as_view(), name='section_update'),
    path('section_delete/<int:pk>', DeleteSection.as_view(), name='section_delete'),
    path('create_announcement', views.create_announcement, name='create_announcement'),
    path('update_announcement/<int:pk>', views.update_announcement, name='update_announcement'),
    path('delete_announcement/<int:pk>', views.delete_announcement, name='delete_announcement'),
    path('approve_accounts', views.approve_accounts, name='approve_accounts'),
    path('ajax/load-sections/', load_sections, name='ajax_load_sections')
]
