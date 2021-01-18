from .models import Category

# assign all categories as list to all_categories variable and after this this value would be reachable from any page in our site
def subject_renderer(request):
    return {
       'all_categories': Category.objects.all(),
    }