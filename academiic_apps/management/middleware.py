from .models import AcademicYear, Quarter


class SiteWideConfigs:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        active_year = AcademicYear.objects.get(active=True)
        active_quarter = Quarter.objects.get(active=True)

        request.active_year = active_year
        request.active_quarter = active_quarter

        response = self.get_response(request)

        return response
