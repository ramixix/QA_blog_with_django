from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    date_posted = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=150)
    snippet = models.CharField(max_length=500)
    body = models.TextField()
    like = models.ManyToManyField(User, blank=True, related_name="likes")
    dislike = models.ManyToManyField(User, blank=True, related_name="dislikes")
    

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog-home')

class Category(models.Model):
    name = models.CharField(max_length=150)
    logo = models.ImageField(default="default.png", upload_to="blog_category")

    def __str__(self):
        return self.name