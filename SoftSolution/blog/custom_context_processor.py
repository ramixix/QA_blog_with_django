from .models import Category

def subject_renderer(request):
    return {
       'all_categories': Category.objects.all(),
    }