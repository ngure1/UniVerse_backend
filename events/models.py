from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator

# Create your models here.
class Event(models.Model):
    author = models.ForeignKey("accounts.UserProfile",on_delete=models.CASCADE, related_name="Event")
    title = models.CharField(max_length=255, default="Default Title")
    description = models.TextField(_("Description"), blank=False)
    created_at = models.DateTimeField(_("Date Created"),auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated_at"),auto_now=True)
    # address = models.OneToOneField("accounts.Address", on_delete=models.CASCADE)
    media = models.FileField(
    _("Event Media"),
    null=True, blank=True,
    upload_to="media/event",
    validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'mp4', 'mov', 'avi'])]
    )
    capacity = models.IntegerField(_("Event's capacity"))

    

    def __str__(self):
        return self.title
