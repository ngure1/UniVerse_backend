from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator

# Create your models here.
class Event(models.Model):
    is_online = models.BooleanField(_("Is Online"), default=False)
    is_physical = models.BooleanField(_("Is Physical"), default=False)
    author = models.ForeignKey("accounts.UserProfile", on_delete=models.CASCADE, related_name="Event")
    title = models.CharField(max_length=255, default="Default Title")
    description = models.TextField(_("Description"), blank=False)
    address = models.CharField(_("Address"), max_length=255, blank=True, null=True)
    venue= models.CharField(_("Venue"), max_length=255, blank=True, null=True)
    media = models.FileField(
    _("Event Media"),
    null=True, blank=True,
    upload_to="media/event",
    validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'mp4', 'mov', 'avi'])]
    )
    event_form_url = models.URLField(_("Event Form URL"), max_length=255, blank=True, null=True)
    event_start_date = models.DateField(_("Event Start Date"), blank=True, null=True)
    event_start_time = models.TimeField(_("Event Start Time"), blank=True, null=True)
    event_end_date = models.DateField(_("Event End Date"), blank=True, null=True)
    event_end_time = models.TimeField(_("Event End Time"), blank=True, null=True)
    created_at = models.DateTimeField(_("Date Created"),auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated_at"),auto_now=True)


    def __str__(self):
        return self.title