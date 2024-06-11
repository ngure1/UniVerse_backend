from django.db import models
from django.contrib.auth.models import  AbstractBaseUser ,PermissionsMixin
from . import managers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


# custom user model
class MyUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model representing a user of the application.
    """

    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = managers.MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.first_name
        """
        Returns a string representation of the user.
        """

# User profile model
class UserProfile(models.Model):
    """
    Model representing a user profile.
    """
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name="user_profile")
    profile_picture = models.ImageField(
        _("Profile Picture"),
        default="default.jpg",
        upload_to="profile_pictures",
        blank=True,
        null=True,
    )
    is_student = models.BooleanField(default=False)
    is_alumni = models.BooleanField(default=False)
    is_lecturer = models.BooleanField(default=False)
    isAdmin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    phone_number = PhoneNumberField(blank=True)
    address = models.OneToOneField("Address", on_delete=models.CASCADE, related_name="profile_address", null=True, blank=True)
    bio = models.TextField(_("Bio"), blank=True)
    linked_in_url = models.URLField(_("LinkedIn Profile"), max_length=100, blank=True, null=True)
    x_in_url = models.URLField(_("X Profile"), max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(_("Date created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Date updated"), auto_now=True)

    def save(self, *args, **kwargs):
        if self.user:
            self.profile_picture.upload_to = f"media/profile_pictures/{self.user.email}"
        super().save(*args, **kwargs)


    def __str__(self):
        """
        Returns a string representation of the user profile.
        """
        return self.user.first_name

    
    def __repr__(self) -> str:
        return self.user.first_name
    
    # Education model
class Education(models.Model):
    owner= models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="education")
    
    institution_name = models.CharField(max_length=255)
    field_of_study = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(_("Date created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Date updated"), auto_now=True)

    def __str__(self):
        return f"{self.field_of_study} from {self.institution_name}"
    
    # Address model
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.postal_code}, {self.country}"


class Follower(models.Model):
    follower = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="following")
    followed = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(_("Date created"), auto_now_add=True)

    class Meta:
        unique_together = ['follower', 'followed']

    def save(self, *args,**kwargs):
        if self.follower == self.followed:
            raise ValidationError({'detail': 'Users cannot follow yourself'})
        super().save(*args,**kwargs)

    def __str__(self):
        return f"{self.follower.user.first_name} follows {self.followed.user.first_name}"
