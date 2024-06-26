from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from rest_framework.exceptions import ValidationError

class Event(models.Model):
    is_online = models.BooleanField(_("Is Online"), default=False)
    is_physical = models.BooleanField(_("Is Physical"), default=False)
    is_attending = models.BooleanField(_("Is Attending"), default=False)
    author = models.ForeignKey("accounts.UserProfile", on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=255, default="Default Title", blank=True, null=True)
    description = models.TextField(_("Description"), blank=False)
    address = models.CharField(_("Address"), max_length=255, blank=True, null=True)
    venue = models.CharField(_("Venue"), max_length=255, blank=True, null=True)
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
    
    created_at = models.DateTimeField(_("Date Created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated_at"), auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Event")
        verbose_name_plural = _("Events")

    def __str__(self):
        return self.title
    
    def clean(self):
        if self.is_online and self.is_physical:
            raise ValidationError(_("An event cannot be both online and physical."))
        if self.event_start_date and self.event_end_date and self.event_start_date > self.event_end_date:
            raise ValidationError(_("Event start date cannot be after event end date."))

class Like(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="event_likes")
    author = models.ForeignKey("accounts.UserProfile", on_delete=models.CASCADE, related_name="author_likes")
    created_at = models.DateTimeField(_("Date created"), auto_now_add=True)

    def __str__(self):
        return f"{self.author.user.first_name} liked {self.event.title}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Like")
        verbose_name_plural = _("Likes")

class Comment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="event_comments")
    author = models.ForeignKey("accounts.UserProfile", on_delete=models.CASCADE, related_name="author_comments")
    text = models.CharField(_("Comment Text"), max_length=255)
    created_at = models.DateTimeField(_("Date created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Date Updated"), auto_now=True)

    def __str__(self):
        return f"{self.author.user.first_name} commented on {self.event.title}: {self.text[:20]}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

class Bookmark(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="event_bookmarks")
    author = models.ForeignKey("accounts.UserProfile", on_delete=models.CASCADE, related_name="author_bookmarks")
    created_at = models.DateTimeField(_("Date Created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Date Updated"), auto_now=True)

    def __str__(self):
        return f"{self.author.user.first_name} bookmarked {self.event.title}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Bookmark")
        verbose_name_plural = _("Bookmarks")
