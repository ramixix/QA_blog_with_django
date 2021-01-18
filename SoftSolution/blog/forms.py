from django import forms
from .models import Post, Category, Comment

# for lising categories in create post page we extracted all of them put them in a list(choices_list)
choices = Category.objects.all().values_list('name', 'name')
choices_list = []
for item in choices:
    choices_list.append(item)

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 'body', 'snippet']

        # pass down the categories list that extracted above and show it as select list 
        widgets = {
            'category' : forms.Select(choices=choices_list)
        }


class NewCommentForm(forms.ModelForm):
    # give some style to comment area and here we assign label to empty string because if we don't it is going to get value 'content' and wirte it as label
    content = forms.CharField(label="", widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Comment here !',
            'rows': 4,
            'cols': 50
        }))

    class Meta:
        model = Comment
        fields = ['content']