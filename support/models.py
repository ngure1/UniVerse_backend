from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator

# Create your models here.

class Support(models.Model):
    owner = models.ForeignKey("accounts.UserProfile", on_delete=models.CASCADE, related_name="support",verbose_name=_("Owner"))
    title = models.CharField(_("Title"),max_length=255)
    description = models.TextField(_("Description"))
    media = models.FileField(
    _("Support Media"),
    null=True, blank=True,
    upload_to="media/support_Media/",
    validators=[ FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'mp4', 'mov', 'avi'])]
    )
    amount = models.DecimalField(_("Amount"),max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(_("Created At"),auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"),auto_now=True)
   
    def save(self, *args, **kwargs):
        if not self.owner.user.is_superuser:
            raise ValidationError(_("Supporter must be an admin."))
        super().save(*args, **kwargs)
   
    def __str__(self):
        return f"{self.title} by {self.owner.user.first_name} {self.owner.user.last_name}"