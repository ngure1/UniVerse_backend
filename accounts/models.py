from django.db import models
from django.contrib.auth.models import  AbstractBaseUser ,PermissionsMixin
from . import managers

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
        """
        Returns a string representation of the user.
        """
        return self.email
