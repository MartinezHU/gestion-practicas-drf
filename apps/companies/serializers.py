from rest_framework import serializers

from .models import Company, CompanyFeatures, Sector


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = "__all__"


class CompanyFeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyFeatures
        fields = "__all__"
        read_only_fields = ("vector_length", "updated_at")


class CompanySerializer(serializers.ModelSerializer):
    sector = SectorSerializer(read_only=True)
    features = CompanyFeaturesSerializer(read_only=True)

    class Meta:
        model = Company
        fields = "__all__"
