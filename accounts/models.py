from django.db import models
from django.contrib.auth.models import  AbstractBaseUser ,PermissionsMixin
from . import managers
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

# custom user model
class CustomUser(AbstractBaseUser, PermissionsMixin):
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

# Address model
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.postal_code}, {self.country}"

# Education model
class Education(models.Model):
    institution_name = models.CharField(max_length=255)
    field_of_study = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.field_of_study} from {self.institution_name}"

# User profile model
class UserProfile(models.Model):
    """
    Model representing a user profile.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(
        _("Profile Picture"),
        upload_to="profile_pictures",
        blank=True,
        null=True,
    )
    is_student = models.BooleanField(default=False)
    is_alumni = models.BooleanField(default=False)
    is_lecturer = models.BooleanField(default=False)
    isAdmin = models.BooleanField(default=False)
    created_at = models.DateTimeField(_("Date created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Date updated"), auto_now=True)
    phone_number = PhoneNumberField(blank=True)
    bio = models.TextField(_("Bio"), blank=True)
    education = models.ForeignKey(Education, on_delete=models.SET_NULL, null=True, blank=True)
    linked_in_url = models.URLField(_("LinkedIn Profile"), max_length=100, blank=True, null=True)
    x_in_url = models.URLField(_("X Profile"), max_length=100, blank=True, null=True)
    superset_url = models.URLField(_("Superset Profile"), max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.user:
            self.profile_picture.upload_to = f"profile_pictures/{self.user.email}"
        super().save(*args, **kwargs)


    def __str__(self):
        """
        Returns a string representation of the user profile.
        """
        return f"{self.user.email}'s profile"

    
    def __repr__(self) -> str:
        return self.user.email
    