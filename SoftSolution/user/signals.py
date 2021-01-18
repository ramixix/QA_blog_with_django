from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

# here after the a user has been registered to the site a defualt profile will be create for that user

# if it recieves a signal from User model (if a user get created it will be save in User table so this table will send signal any time a user get created)
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    # any time we get that singal we check if a user is created and it's true then create a profile in database with user of who own that signal
    if created:
        Profile.objects.create(user=instance)

# after making profile for new registered user we need to save it to database
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()