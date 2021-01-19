from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django.db.models import Q
# Create your models here.




class BlogPostQuerySet(models.QuerySet):
    def search(self, query):
        # search according to title, body, category, snippet of posts, also username, firstname, lastname, email of users
        search_area = (
                Q(title__icontains=query) |
                Q(body__icontains=query) |
                Q(category__icontains=query) |
                Q(author__username__icontains=query) |
                Q(author__first_name__icontains=query) |
                Q(author__last_name__icontains=query) |
                Q(snippet__icontains=query) |
                Q(author__email__icontains=query)
        )
        return self.filter(search_area)

class BlogPostManager(models.Manager):
    def get_queryset(self):
        return BlogPostQuerySet(self.model, using=self._db)

    def search(self, query=None):
        # checks the query to not be empty
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().search(query)


# model for saving posts to database
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
    objects = BlogPostManager()

    def __str__(self):
        return self.title

    # used to redirect users to home page after creating a post or deleting one
    def get_absolute_url(self):
        return reverse('blog-home')

    # fucntion that returns total like of a post, used in PostDetailView, LikeView ...
    def all_likes(self):
        return self.like.count()

    def all_dislikes(self):
        return self.dislike.count()

    # function that returns total number of comments that have been made on a specific post(used in detail_post.html)
    @property
    def number_of_comments(self):
        return Comment.objects.filter(post=self).count()


# model to save added categories (cateogries can added just by admin)
class Category(models.Model):
    name = models.CharField(max_length=150)
    logo = models.ImageField(default="default.png", upload_to="blog_category")

    def __str__(self):
        return self.name


# model to save comments
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    like = models.ManyToManyField(User, blank=True, related_name="comment_like")
    dislike = models.ManyToManyField(User, blank=True, related_name="comment_dislike")
    comment_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{str(self.post.title)}-{str(self.user.username)}'

    # redirect user after creating a comment to the post that user made comment on
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={ 'pk' : self.pk })

    def all_likes(self):
        return self.like.count()

    def all_dislikes(self):
        return self.dislike.count()