from django import forms
from .models import Post, Category

choices = Category.objects.all().values_list('name', 'name')
choices_list = []
for item in choices:
    choices_list.append(item)

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 'body', 'snippet']

        widgets = {
            'category' : forms.Select(choices=choices_list)
        }