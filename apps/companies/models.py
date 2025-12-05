from django.db import models


class Sector(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)


class Company(models.Model):
    name = models.CharField(max_length=50)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    location = models.TextField()
    skill_requirements = models.JSONField()
    company_size = models.CharField(max_length=50)
    founded_year = models.IntegerField(blank=True, null=True)
    num_employees = models.IntegerField(blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class CompanyFeatures(models.Model):
    company = models.OneToOneField(
        Company, on_delete=models.CASCADE, related_name="features"
    )
    skills_vector = models.JSONField()
    availability_places = models.IntegerField()
    historical_success_rate = models.FloatField()
    vector_length = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Features for {self.company.name}"
