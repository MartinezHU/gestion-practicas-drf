from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    SEX_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other/I prefer not to say"),
    )
    gender = models.CharField(max_length=10, choices=SEX_CHOICES)
    course_year = models.IntegerField(blank=True, null=True)
    academy_training = models.TextField()
    speciality = models.CharField(max_length=100)
    skills = models.JSONField()
    num_skills = models.IntegerField(blank=True, null=True)
    availability = models.BooleanField(default=True)
    AVAILABILITY_CHOICES = (
        ("full-time", "Full Time"),
        ("part-time", "Part Time"),
        ("mornings", "Mornings"),
        ("afternoons", "Afternoons"),
        ("evenings", "Evenings"),
    )
    availability_type = models.CharField(
        max_length=20, choices=AVAILABILITY_CHOICES, blank=True, null=True
    )

    def __str__(self):
        return f"{self.name} {self.last_name}"


class StudentFeatures(models.Model):
    student = models.OneToOneField(
        Student, on_delete=models.CASCADE, related_name="features"
    )
    skills_vector = models.JSONField()
    success_probability = models.FloatField(null=True, blank=True)
    availability = models.BooleanField(default=True)
    availability_type = models.CharField(max_length=20, blank=True, null=True)
    vector_length = models.IntegerField(blank=True, null=True)  # derivado
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Features for {self.student.name} {self.student.last_name}"
