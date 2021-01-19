from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(default='default.jpg', upload_to="profile_img")
    education = models.CharField(max_length=255, blank=True, null=True)
    website_url = models.CharField(max_length=255, blank=True, null=True)
    linkin_url = models.CharField(max_length=255, blank=True, null=True)
    facebook_url = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username}_profile'

    # overwirte the save function jsut because some profile pictures can be very big pictures
    # so here pictures are tested, and if they have more than 300 pixels in height or width 
    # they are going to be resize and then save to our database
    def save(self, *args, **kwargs):
        super().save(*args, **  kwargs)

        img = Image.open(self.image.path)
        if img.width > 300 or img.height > 300:
            final_size = (300, 300)
            img.thumbnail(final_size)
            img.save(self.image.path)