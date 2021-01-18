"""SoftSolution URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_view
from django.conf import settings
from django.conf.urls.static import static
from searches.views import search_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("blog.urls")),
    path('user/', include("user.urls")),
    # loign and logout classes are inheritanced from auth views, we used default forms of this pages(just added template name to add ours html files)
    path('login/', auth_view.LoginView.as_view(template_name="user/login.html"), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='user/logout.html'), name='logout'),
    path('search/', search_view)

]
# for displaying medias in debug mode it is needed to add this line of code, it adds the media directory to urlpatterens list 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)