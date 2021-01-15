from django.contrib.auth.models import User
from .models import Post, Category
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from .forms import PostCreateForm
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
# Create your views here.

class Homeview(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = 'posts'
    ordering = ["-date_posted"]
    paginate_by = 5

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
    paginate_by = 2

    def test_func(self):
        if (Category.objects.filter(name=self.kwargs.get('cat')).exists()):
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryView, self).get_context_data(*args, **kwargs)
        posts = Post.objects.filter(category=self.kwargs.get('cat'))
        num_posts = posts.count()
        paginator = Paginator(posts, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
            
        context['page_obj'] = posts
        context['num_posts'] = num_posts
        return context

class UserProfileView(ListView):
    model = User
    template_name = "blog/user_profile.html"           
    context_object_name = "user" 

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return user
    
    def get_context_data(self, *args, **kwargs):
        context = super(UserProfileView, self).get_context_data(*args, **kwargs)
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        context['posts'] = Post.objects.filter(author=user.id)
        return context