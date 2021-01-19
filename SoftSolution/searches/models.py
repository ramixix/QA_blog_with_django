from django.db import models
from django.conf import settings


# search model for getting what searches asked and saving searches to database as log
class SearchQuery(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete= models.SET_NULL)
	query = models.CharField(max_length=256)
	timestamp = models.DateTimeField(auto_now_add=True)


	def __str__(self):
	        return '{}-{}'.format(self.query, str(self.timestamp))