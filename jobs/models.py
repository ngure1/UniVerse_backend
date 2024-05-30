from django.db import models
from django.utils import timezone


class Job(models.Model):
    job_owner = models.ForeignKey("accounts.UserProfile", on_delete=models.CASCADE, related_name="jobs")
    title = models.CharField(max_length=255)
    description = models.TextField()
    application_deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    application_procedure = models.TextField()

    def __str__(self):
        return self.title

    def is_application_open(self):
        return timezone.now() < self.application_deadline

    def extend_deadline(self, new_deadline):
        if new_deadline > self.application_deadline:
            self.application_deadline = new_deadline
            self.save()
        else:
            raise ValueError("New deadline must be later than the current deadline.")
