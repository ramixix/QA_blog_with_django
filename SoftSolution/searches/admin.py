from django.contrib import admin
from .models import SearchQuery

# adding search model to admin page to be able display the search logs in admin site 
admin.site.register(SearchQuery)