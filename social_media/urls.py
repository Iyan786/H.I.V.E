"""
URL configuration for social_media project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path,include
from social import views 
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.add_post,name='index'),
    path('reg', views.reg,name='reg'),
    path('loginpage', views.loginpage,name='loginpage'),
    path('editprofile', views.editprofile,name='editprofile'),
    path('dashboard', views.dashboard,name='dashboard'),
    path('users', views.users,name='users'), 
    path('post/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('apost/delete/<int:post_id>/', views.adelete_post, name='adelete_post'),
    path('delete_user/<int:id>/', views.delete_user, name='delete_user'),
    path('logout/', views.user_logout, name='logout'),
    path('edit_pass/', views.edit_pass, name='edit_pass'),
    path('profile/', views.profile, name='profile'),
    path('messages1/<str:receiver_username>/', views.messages1, name='messages1'),
    # path('update-logo/',views.update_logo, name='update_logo')
    path('chat/<str:receiver_username>/', views.chat_view, name="chat"),
    path('manage_post/', views.manage_post, name="manage_post"),
    path('feed/', views.feed, name="feed"),
    path("user/<int:user_id>/", views.user_detail_view, name="user-detail"),
    path("post/<int:post_id>/ban/", views.ban_post, name="ban-post"),
    path("post/<int:post_id>/unban/", views.unban_post, name="unban-post"),
    path('increment-views/<int:post_id>/', views.increment_views, name='increment_views'),
    path('like-post/<int:post_id>/', views.like_post, name='like_post'),
    path('dislike-post/<int:post_id>/', views.dislike_post, name='dislike_post'),
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
