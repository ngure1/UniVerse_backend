from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator


class Job(models.Model):
    ONLINE = 'online'
    PHYSICAL = 'physical'
    BOTH = 'both'
    JOB_TYPE_CHOICES = [
        (ONLINE, 'Online'),
        (PHYSICAL, 'Physical'),
        (BOTH, 'Both'),
    ]
    
    author = models.ForeignKey("accounts.UserProfile", on_delete=models.CASCADE, related_name="jobs", verbose_name=_("Job Owner"))
    job_title=models.CharField(_("Job Title"), max_length=255)
    job_description = models.TextField(_("Description"))
    job_skills=models.TextField(_("Skills"), blank=True, null=True)
    job_qualifications=models.TextField(_("Qualifications"), blank=True, null=True)
    job_type = models.CharField(
        _("Job Type"),
        max_length=10,
        choices=JOB_TYPE_CHOICES,
        default=PHYSICAL,
        help_text=_("Select the type of job (Online, Physical, or Both).")
        )
    address=models.CharField(_("Address"), max_length=255, blank=True, null=True)
    media = models.FileField(
    _("Job Media"),
    null=True, blank=True,
    upload_to="media/Job_Media",
    validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'mp4', 'mov', 'avi'])]
    )
    application_deadline = models.DateTimeField(_("Application Deadline"))
    application_procedure = models.TextField(_("Application Procedure"))
    application_link = models.URLField(_("Application Link"), max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(_("Date Created "),auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"),auto_now=True)


    def __str__(self):
        return self.title

    def is_application_open(self):
        return timezone.now() < self.application_deadline

    def extend_deadline(self, new_deadline):
        if new_deadline > self.application_deadline:
            self.application_deadline = new_deadline
            self.save()
        else:
            raise ValueError(_("New deadline must be later than the current deadline."))
