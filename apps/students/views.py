from rest_framework import viewsets, filters

from .models import Student, StudentFeatures
from .serializers import StudentSerializer, StudentFeaturesSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "last_name", "email", "speciality"]
    ordering_fields = ["date_of_birth", "course_year", "last_name"]


class StudentFeaturesViewSet(viewsets.ModelViewSet):
    queryset = StudentFeatures.objects.all()
    serializer_class = StudentFeaturesSerializer
