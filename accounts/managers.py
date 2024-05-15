from django.contrib.auth.models import BaseUserManager

class MyUserManager(BaseUserManager):
    # Method to create a regular user
    def create_user(self, email, password=None , **kwargs):
        # Check if email is provided
        if not email:
            raise ValueError("Users must have an email address")

        # Normalize the email by making the domain part of the email lowercase
        email=self.normalize_email(email)

        # Create a user instance
        user = self.model(
            email = email.lower(),  # set email
            password = password,  # set password
            **kwargs,  # set any additional fields
        )

        # Set user password, this also handles password hashing
        user.set_password(password)
        # Save the user object to the database
        user.save(using=self._db)
        # Return the user object
        return user

    # Method to create a superuser or admin
    def create_superuser(self, email,  password=None , **kwargs):
        # Create a user instance
        user = self.create_user(
            email,
            password=password,
            **kwargs
        )

        # Set the admin-related fields to True
        user.is_staff = True
        user.is_superuser = True
        # Save the user object to the database
        user.save(using=self._db)
        return user