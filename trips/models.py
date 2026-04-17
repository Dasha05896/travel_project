from django.db import models
from django.core.exceptions import ValidationError

class TravelProject(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if self.places.filter(is_visited=True).exists():
            raise ValidationError("Cannot delete a project with visited places.")
        super().delete(*args, **kwargs)

class Place(models.Model):
    project = models.ForeignKey(
        TravelProject,
        related_name="places",
        on_delete=models.CASCADE
    )
    external_id = models.IntegerField()
    notes = models.TextField(blank=True, null=True)
    is_visited = models.BooleanField(default=False)

    class Meta:
        unique_together = ("project", "external_id")

    def __str__(self):
        return f"Place {self.external_id} in {self.project.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        project = self.project
        if project.places.exists() and not project.places.filter(is_visited=False).exists():
            project.is_completed = True
            project.save()
