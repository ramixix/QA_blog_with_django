from django.contrib.auth.models import User                                                 #importing the user model to use it in different veiw pages
from .models import Post, Category, Comment                                                 #importing the models that we have created from blog.models.py
from django.shortcuts import render, get_object_or_404,redirect                              
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView   #importing bulid in views to use them
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin              #this two are the classes that help us to make sure a user is login before be able to enter in specific page
from django.urls import reverse_lazy, reverse               
from .forms import PostCreateForm, NewCommentForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.template.loader import render_to_string
# the next three classes are imported for pagination post that are in specific categories look at CategoryView class
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

# class for our main page, we show our posts in this page, used pagintion to show 5 posts per page in reverse ordering that they are created 
class Homeview(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = 'posts'
    ordering = ["-date_posted"]
    paginate_by = 8

def About(request):
    return render(request, 'blog/about.html')


# class for post creation we did inheritance LoginRequiredMixin class to make sure that users are login before be able to open this page
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/create_post.html'
    form_class = PostCreateForm

    # form_valid function is used to assign the user who is trying create the post to author of that post automatically without them knowing. 
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# class for veiwing a post in detail 
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail_post.html'
    
    # here we pss some date like comments of that post, total likes and dislike to detail_post.html for showing them in that page 
    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        current_post = get_object_or_404(Post, id=self.kwargs.get('pk'))
        comments_connected = Comment.objects.filter(post= self.get_object()).order_by('-comment_time')
        #context['comments'] = Comment.objects.filter(post=current_post)
        context['all_dislikes'] = current_post.all_dislikes()
        context['all_likes'] = current_post.all_likes()
        context['comments'] = comments_connected
        # pass comment form that we made in form.py
        context['comment_form'] = NewCommentForm()

        return context

    # if the method is post then take the comment and save it to the datebase and return user to same post detail
    def post(self, request, *args, **kwargs):

        new_comment = Comment(content=request.POST.get('content'), user=self.request.user, post=self.get_object())
        new_comment.save()
        return HttpResponseRedirect(reverse("post-detail",kwargs={'pk':self.kwargs.get('pk')}))


# class for updating posts that have been maden
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/create_post.html'
    fields = ['title', 'category', 'body', 'snippet']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # test_func is used to make sure that users can just update their own posts 
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author :
            return True
        return False


# class for deleteing post that have been maden
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    success_url = reverse_lazy('blog-home')
     
    # test_func is used to make sure that users can just delete their own posts 
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author :
            return True
        return False


# class for posts that are only in a specific category
class CategoryView(UserPassesTestMixin, ListView):
    model = Post
    template_name = "blog/categories.html"
    ordering = ["-date_posted"]
    paginate_by = 5

    def test_func(self):
        if (Category.objects.filter(name=self.kwargs.get('cat')).exists()):
            return True
        return False
    
    # we passed the necessary data for category page and used Paginator, PageNotAnInteger, EmptyPage classes to paginate posts in specific categories
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


# class for showing other users profile 
class UserProfileView(ListView):
    model = User
    template_name = "blog/user_profile.html"           
    context_object_name = "user" 

    # get_queryset function is for get the specific user form the information passed to url
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return user
    
    # get_context_data is used to pass the posts that have been made by that user, used to show what posts a user has been made, in his/her profile page
    def get_context_data(self, *args, **kwargs):
        context = super(UserProfileView, self).get_context_data(*args, **kwargs)
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        context['posts'] = Post.objects.filter(author=user.id)
        return context


# function to save data about the likes in database after some users click on like button of a post
def LikeView(request, pk):
    post = get_object_or_404(Post, id=pk)
    # after finding the specific post form the url, it checks if the current user has been like that post
    if post.like.filter(id=request.user.id).exists():
        post.like.remove(request.user)
    # here it checks if the current user has been dislike the post
    elif post.dislike.filter(id=request.user.id).exists():
        post.dislike.remove(request.user)
        post.like.add(request.user)
    else:
        post.like.add(request.user)
    # take post, and its total like and dislike for passing to ajax function that is been written in post_detail.html
    context = {
        'object' : post,
        'all_likes' : post.all_likes(),
        'all_dislikes' : post.all_dislikes(),
    }

    if request.is_ajax():
        # taking the like_seciton.html page and render it to string and after that pass it to ajax in json form
        html = render_to_string('blog/like_section.html', context, request=request)

        return JsonResponse({'form':html})


# function to save data about the dislikes in database after some users click on dislike button of a post, works similar to like button that explained one function above
def DisLikeView(request, pk):
    post = get_object_or_404(Post, id=pk)
    if post.dislike.filter(id=request.user.id).exists():
        post.dislike.remove(request.user)
    elif post.like.filter(id=request.user.id).exists():
        post.like.remove(request.user)
        post.dislike.add(request.user)
    else:
        post.dislike.add(request.user)
    
    context = {
        'object' : post,
        'all_likes' : post.all_likes(),
        'all_dislikes' : post.all_dislikes(),
    }

    if request.is_ajax():
        html = render_to_string('blog/like_section.html', context, request=request)
        return JsonResponse({'form':html})


# function to save data about the likes in database after some users click on dislike button of a comment, works similar to like and dislike post fucntions
def CommentLikeView(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    comments = Comment.objects.filter(post_id=comment.post.id).order_by('-comment_time')

    if comment.like.filter(id=request.user.id).exists():
        comment.like.remove(request.user)
    elif comment.dislike.filter(id=request.user.id).exists():
        comment.dislike.remove(request.user)
        comment.like.add(request.user)
    else:
        comment.like.add(request.user)

    context = {
        'comments':comments,
    }


    if request.is_ajax():
            html = render_to_string('blog/comment_like_section.html',context,request=request)
            return JsonResponse({'form': html})


# function to save data about the dislikes in database after some users click on dislike button of a comment, works similar to like and dislike post fucntions
def CommentDisLikeView(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    comments = Comment.objects.filter(post_id=comment.post.id).order_by('-comment_time')

    if comment.dislike.filter(id=request.user.id).exists():
        comment.dislike.remove(request.user)
    elif comment.like.filter(id=request.user.id).exists():
        comment.like.remove(request.user)
        comment.dislike.add(request.user)
    else:
        comment.dislike.add(request.user)

    context = {
        'comments': comments,
    }

    if request.is_ajax():
        html = render_to_string('blog/comment_like_section.html', context, request=request)
        return JsonResponse({'form': html})

