from academiic_apps.core.models import SiteConfig
from academiic_apps.management.models import Level, Section, Quarter, AcademicYear


def site_defaults(request):
    active_year = AcademicYear.objects.get(active=True)
    active_quarter = Quarter.objects.get(active=True)
    vals = SiteConfig.objects.all()
    contexts = {
        "active_year": active_year.academic_Year,
        "active_quarter": active_quarter.quarter,
    }
    for val in vals:
        contexts[val.key] = val.value

    return contexts


def level_list(request):
    levels = Level.objects.all()
    sections = Section.objects.all()
    return {"levels": levels, "sections": sections}
