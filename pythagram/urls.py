"""instagram URL Configuration

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
from django.urls import path

from posts import views as post_views
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

handler403 = 'posts.views.handler403'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', post_views.home, name='home'),
    path('about/', post_views.about, name='about'),
    path('login/', post_views.Login.as_view(template_name='posts/login.html'), name='login'),
    path('register/', post_views.register, name='register'),
    path('logout/', post_views.Logout.as_view(), name='logout'),
    path('profile/update/', post_views.profileUpdate, name='profile-update'),
    path('profile/<username>/', post_views.ViewProfile.as_view(), name='profile'),
    path('profile/<str:username>/follow/', post_views.followUser, name='follow-user'),
    path('posts/new/', post_views.CreatePost.as_view(), name='create-post'),
    path('post/<int:pk>/', post_views.viewPost, name='view-post'),
    path('post/<int:pk>/like/', post_views.likePost, name='like-post'),
    path('post/<int:pk>/update/', post_views.postUpdate, name='update-post'),
    path('post/<int:pk>/delete/', post_views.postDeleteForm, name='delete-post'),
    path('comment/<int:pk>/update/', post_views.commentUpdate, name='update-comment'),
    path('comment/<int:pk>/delete/', post_views.commentDelete, name='delete-comment'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='posts/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='posts/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
             auth_views.PasswordResetConfirmView.as_view(template_name='posts/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='posts/password_reset_complete.html'),
         name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)