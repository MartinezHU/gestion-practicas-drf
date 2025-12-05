from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.companies.views import CompanyViewSet, CompanyFeaturesViewSet, SectorViewSet
from apps.core.views import APIUserViewSet
from apps.internships.views import InternshipViewSet, DailyLogViewSet
from apps.matches.views import PredictedMatchViewSet, HistoricalMatchesViewSet, MatchLogViewSet
from apps.students.views import StudentViewSet, StudentFeaturesViewSet

router = DefaultRouter()

# Viewsets

router.register(r'users', APIUserViewSet)

# Students
router.register(r'students', StudentViewSet)
router.register(r'student-features', StudentFeaturesViewSet)
# Companies
router.register(r'companies', CompanyViewSet)
router.register(r'company-features', CompanyFeaturesViewSet)
router.register(r'sectors', SectorViewSet)
# Internships
router.register(r'internships', InternshipViewSet)
router.register(r'daily-logs', DailyLogViewSet)
# Matches
router.register(r'predicted-matches', PredictedMatchViewSet)
router.register(r'historical-matches', HistoricalMatchesViewSet)
router.register(r'match-logs', MatchLogViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("rest-auth/", include("rest_framework.urls")),
    path('api/', include(router.urls))
]
