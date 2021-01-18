from django.contrib import admin
from .models import Post, Category,Comment

# register all three models that have been made to admin page
admin.site.register(Post)

admin.site.register(Category)

admin.site.register(Comment)
