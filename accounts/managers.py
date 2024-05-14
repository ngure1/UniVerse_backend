from django.contrib.auth.models import BaseUserManager

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