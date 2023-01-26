"""academiic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("academiic_apps.core.urls")),
    path('faculties/', include("academiic_apps.faculty.urls")),
    path('grades/', include("academiic_apps.grading.urls")),
    path('billing/', include("academiic_apps.billing.urls")),
    path('management/', include("academiic_apps.management.urls")),
    path('students/', include("academiic_apps.student.urls")),
    path('subjects/', include("academiic_apps.subjects.urls", namespace='subjects'))
]
