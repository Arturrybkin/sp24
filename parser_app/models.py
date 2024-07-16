from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    salary = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} at {self.company_name}"

