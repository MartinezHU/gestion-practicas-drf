from django.db import models

from apps.companies.models import Company
from apps.students.models import Student


class HistoricalMatches(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="historical_matches"
    )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="historical_matches"
    )
    result = models.BooleanField()
    actual_duration_of_internships = models.IntegerField(
        help_text="Duración real de la práctica en horas o semanas"
    )
    notes = models.TextField(blank=True, null=True)
    student_age = models.IntegerField(blank=True, null=True)
    company_sector = models.CharField(max_length=50, blank=True, null=True)
    match_score = models.FloatField(blank=True, null=True)
    match_type = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.student} ↔ {self.company} ({'Éxito' if self.result else 'Fracaso'})"
        )


class PredictedMatch(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="predicted_matches"
    )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="predicted_matches"
    )
    score = models.FloatField()
    student_age = models.IntegerField(blank=True, null=True)
    student_year = models.IntegerField(blank=True, null=True)
    num_skills = models.IntegerField(blank=True, null=True)
    company_sector = models.CharField(max_length=50, blank=True, null=True)
    company_size = models.CharField(max_length=50, blank=True, null=True)
    applied = models.BooleanField(default=False)
    status_choices = (
        ("pending", "Pending"),
        ("applied", "Applied"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    )
    status = models.CharField(max_length=20, choices=status_choices, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("student", "company")

    def __str__(self):
        return f"{self.student} ↔ {self.company} ({self.score})"


class MatchLog(models.Model):
    predicted_match = models.ForeignKey(
        PredictedMatch, on_delete=models.CASCADE, related_name="logs"
    )
    features_used = models.JSONField()
    score = models.FloatField()
    matching_algorithm_version = models.CharField(max_length=10, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log for {self.predicted_match}"
