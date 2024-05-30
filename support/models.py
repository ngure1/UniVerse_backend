from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.

class Support(models.Model):
    owner = models.ForeignKey("accounts.UserProfile", on_delete=models.CASCADE, related_name="support")
    title = models.CharField(max_length=255)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   
    def save(self, *args, **kwargs):
        if not self.owner.user.is_superuser:
            raise ValidationError("Supporter must be an admin.")
        super().save(*args, **kwargs)
   
    def __str__(self):
        return f"{self.title} by {self.owner.user.first_name} {self.owner.user.last_name}"