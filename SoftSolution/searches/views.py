from django.shortcuts import render
from .models import SearchQuery
from blog.models import Post, BlogPostManager


# Create your views here.

# search view takes the query that users pass to search bar and display the resualts
def search_view(request):
	query = request.GET.get('q', None)
	user = None
	if request.user.is_authenticated:
		user = request.user

	context = {"query":query}
	# if query that user passed was not an empty string log that query to database and class search funtion
	if query is not None:
		SearchQuery.objects.create(user=user, query=query)
		blog_list = Post.objects.search(query=query)
		context['blog_list'] = blog_list

	

	return render(request, 'searches/view.html', context)