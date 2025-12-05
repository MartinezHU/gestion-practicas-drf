from rest_framework import viewsets, filters

from .models import Company, CompanyFeatures, Sector
from .serializers import CompanySerializer, CompanyFeaturesSerializer, SectorSerializer


class SectorViewSet(viewsets.ModelViewSet):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer


class CompanyFeaturesViewSet(viewsets.ModelViewSet):
    queryset = CompanyFeatures.objects.all()
    serializer_class = CompanyFeaturesSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "sector__name", "location"]
    ordering_fields = ["name", "company_size", "founded_year"]
