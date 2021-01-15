from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Post,Category
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from .forms import PostCreateForm
# Create your views here.

class Homeview(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = 'posts'
    ordering = ["-date_posted"]

def About(request):
    return render(request, 'blog/about.html')


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/create_post.html'
    form_class = PostCreateForm


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail_post.html'


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/create_post.html'
    fields = ['title', 'category', 'body', 'snippet']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author :
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    success_url = reverse_lazy('blog-home')

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author :
            return True
        return False


class CategoryView(UserPassesTestMixin, ListView):
    model = Post
    template_name = "blog/categories.html"
    ordering = ["-date_posted"]

    def test_func(self):
        if (Category.objects.filter(name=self.kwargs.get('cat')).exists()):
            return True
        return False


    def get_context_data(self, *args, **kwargs):
        context = super(CategoryView, self).get_context_data(*args, **kwargs)
        posts = Post.objects.filter(category=self.kwargs.get('cat'))

        context['posts'] = posts
        return context