from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import PredictedMatch, HistoricalMatches, MatchLog
from .serializers import (
    PredictedMatchSerializer,
    HistoricalMatchesSerializer,
    MatchLogSerializer,
)


class MatchLogViewSet(viewsets.ModelViewSet):
    queryset = MatchLog.objects.all()
    serializer_class = MatchLogSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["timestamp", "score"]


class PredictedMatchViewSet(viewsets.ModelViewSet):
    queryset = PredictedMatch.objects.all()
    serializer_class = PredictedMatchSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["student__name", "student__last_name", "company__name"]
    ordering_fields = ["score", "created_at"]

    @action(detail=True, methods=["post"])
    def mark_applied(self, request, pk=None):
        match = self.get_object()
        match.applied = True
        match.status = "applied"
        match.save()
        return Response({"status": "marked as applied"})


class HistoricalMatchesViewSet(viewsets.ModelViewSet):
    queryset = HistoricalMatches.objects.all()
    serializer_class = HistoricalMatchesSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["student__name", "student__last_name", "company__name"]
    ordering_fields = ["created_at", "actual_duration_of_internships"]
