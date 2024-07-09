from django.db.models.signals import post_save 
from django.dispatch import receiver
from .models import MyUser, UserProfile, Address


@receiver(post_save, sender=MyUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=MyUser)
def save_user_profile(sender, instance , **kwargs):
    instance.user_profile.save()


@receiver(post_save, sender=UserProfile)
def create_address_for_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create an Address instance with its fields, leaving them empty or with default values
        address = Address.objects.create()
        
        # Link the created Address to the UserProfile
        instance.address = address
        instance.save()

