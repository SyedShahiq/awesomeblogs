"""blog_admin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from blog.views import home_view,posts_view,single_post_view,fetchAllPosts,posts_by_user,add_emotion,edit_posts,create_posts,delete_post
from user_profile.views import user_registration,fetch_user_detail
from comments.views import createNewReply
from django.contrib.auth import views as auth_views

urlpatterns = [
	path('',home_view,name='home'),
	path('posts/',posts_view,name='posts'),
    path('api/posts/',fetchAllPosts,name='api-posts'),
    path('post/<int:id>',single_post_view,name='single-post'),
    path('post/user/<int:id>',posts_by_user,name='post-by-users'),
    path('post/edit/<int:id>',edit_posts,name="post-edit"),
    path('post/create/',create_posts,name='post-create'),
    path('post/delete/<int:id>',delete_post,name='delete-post'),
    path('create-new-reply/',createNewReply,name='new-reply'),
    path('user/register/',user_registration,name='user-register'),
    path('logout/',auth_views.logout,name="logout"),
    path('login/',auth_views.LoginView.as_view(template_name='login.html'),name="Login"),
    path('like/<int:id>',add_emotion,name="like"),
    path('api/user/<int:id>',fetch_user_detail,name='user-details'),
    path('admin/', admin.site.urls),
]
