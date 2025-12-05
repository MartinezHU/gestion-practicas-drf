from datetime import date

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from apps.companies.models import Company
from apps.students.models import Student


class Internship(models.Model):
    student = models.OneToOneField(
        Student, on_delete=models.CASCADE, related_name="internship"
    )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="internships"
    )
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    total_hours_planned = models.IntegerField()
    actual_hours_completed = models.IntegerField(blank=True, null=True)
    company_mentor = models.CharField(max_length=100)
    internship_type = models.CharField(
        max_length=20, blank=True, null=True
    )  # on-site/remote/hybrid
    final_tutor_valuation = models.FloatField(blank=True, null=True)
    duration_weeks = models.FloatField(blank=True, null=True)

    INTERNSHIP_STATE_CHOICES = (
        ("planned", "Planned"),
        ("ongoing", "Ongoing"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    )
    state = models.CharField(
        max_length=20, choices=INTERNSHIP_STATE_CHOICES, default="planned"
    )

    def __str__(self):
        return f"{self.student} @ {self.company} ({self.state})"


class DailyLog(models.Model):
    internship = models.ForeignKey(
        Internship, on_delete=models.CASCADE, related_name="daily_logs"
    )
    date = models.DateField(default=date.today)
    hours_performed = models.IntegerField(validators=[MinValueValidator(0)])
    cumulative_hours = models.IntegerField(blank=True, null=True)
    day_of_week = models.IntegerField(blank=True, null=True)
    is_weekend = models.BooleanField(blank=True, null=True)
    activities = models.TextField()
    tutor_valuation = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    emotional_state = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Log {self.date} - {self.internship.student.name}"
