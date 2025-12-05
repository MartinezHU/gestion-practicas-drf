from rest_framework import serializers

from .models import PredictedMatch, HistoricalMatches, MatchLog


class MatchLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchLog
        fields = "__all__"


class PredictedMatchSerializer(serializers.ModelSerializer):
    logs = MatchLogSerializer(many=True, read_only=True)

    class Meta:
        model = PredictedMatch
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")

    @staticmethod
    def validate_score(value):
        if not (0 <= value <= 1):
            raise serializers.ValidationError("El score debe estar entre 0 y 1")
        return value


class HistoricalMatchesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalMatches
        fields = "__all__"
        read_only_fields = ("created_at",)
