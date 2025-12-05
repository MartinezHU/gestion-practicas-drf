from rest_framework import viewsets, filters

from .models import Internship, DailyLog
from .serializers import InternshipSerializer, DailyLogSerializer


class DailyLogViewSet(viewsets.ModelViewSet):
    queryset = DailyLog.objects.all()
    serializer_class = DailyLogSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["date", "hours_performed"]


class InternshipViewSet(viewsets.ModelViewSet):
    queryset = Internship.objects.all()
    serializer_class = InternshipSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["student__name", "student__last_name", "company__name"]
    ordering_fields = ["start_date", "end_date", "total_hours_planned"]
