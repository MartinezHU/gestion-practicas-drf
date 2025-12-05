from rest_framework import serializers

from .models import Student, StudentFeatures


class StudentFeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentFeatures
        fields = "__all__"
        read_only_fields = ("vector_length", "updated_at")  # derivado, solo lectura


class StudentSerializer(serializers.ModelSerializer):
    features = StudentFeaturesSerializer(read_only=True)  # anidado

    class Meta:
        model = Student
        fields = "__all__"
        read_only_fields = ("num_skills",)  # calculado a partir de skills

    @staticmethod
    def validate_email(value):
        if not "@" in value:
            raise serializers.ValidationError("Email inválido")
        return value
