from rest_framework import serializers
from .models import Internship, DailyLog


class DailyLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyLog
        fields = "__all__"
        read_only_fields = ("cumulative_hours", "day_of_week", "is_weekend")


class InternshipSerializer(serializers.ModelSerializer):
    daily_logs = DailyLogSerializer(many=True, read_only=True)

    class Meta:
        model = Internship
        fields = "__all__"

    def validate(self, data):
        start = data.get("start_date")
        end = data.get("end_date")
        if end and start > end:
            raise serializers.ValidationError(
                "La fecha de inicio no puede ser posterior a la fecha de fin"
            )
        return data
