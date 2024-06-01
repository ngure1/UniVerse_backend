from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
# Create your models here.


class Announcement(models.Model):
    creator = models.ForeignKey("accounts.UserProfile", on_delete=models.CASCADE, related_name="announcements")
    title = models.CharField(_("Announcement Title"),max_length=255)
    content = models.TextField(_("Announcement contents"))
    created_at = models.DateTimeField(_("Date Created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Date Updated"), auto_now=True)
    media = models.ImageField(_("Announcement Media"), upload_to='announcements', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.creator.user.is_superuser:
            raise ValidationError(_("Only Admins can create announcements"))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


