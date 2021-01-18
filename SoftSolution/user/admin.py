from django.contrib import admin
from .models import Profile

# Register profile model to admin page
admin.site.register(Profile)