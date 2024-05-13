from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser ,PermissionsMixin


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None , **kwargs):
        if not email:
            raise ValueError("Users must have an email address")

        email=self.normalize_email(email)

        user = self.model(
            email = email.lower(),
            password = password,
            **kwargs,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,  password=None , **kwargs):
        
        user = self.create_user(
            email,
            password=password,
            **kwargs
        )

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(max_length=255,unique=True,)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)


    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name","last_name"]

    def __str__(self):
        return self.email
