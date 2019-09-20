from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import TemplateView, FormView
from django.shortcuts import render, redirect
from .forms import (UserUpdateForm,
                    ProfileUpdateForm,
                    PostUpdateForm,
                    CommentUpdateForm,
                    CommentDeleteForm,
                    PostDeleteForm
                    )

from .forms import UserRegisterForm, PostForm, CommentForm
from .middleware import AuthRequiredMiddleware
from .models import Post, Comment
import boto3


pathList = []

def handler403(request, exception):
    messages.error(
        request,
        f'You have no permission to do that'
    )
    return redirect('/')

def pathRecords(newPath):
    pathList.append(newPath)
    if len(pathList) > 2:
        pathList.pop(0)
    return pathList

def home(request):
    path = pathRecords(request.path)
    posts = Post.objects.all().order_by('-date_posted')
    comments = Comment

    # -- PAGINATION START-- #
    postList = Post.objects.all().order_by('-date_posted')
    page = request.GET.get('page', 1)
    paginator = Paginator(postList, 6)
    try:
        postList = paginator.page(page)
    except PageNotAnInteger:
        postList = paginator.page(1)
    except EmptyPage:
        postList = paginator.page(paginator.num_pages)
    # -- PAGINATION END -- #
    likes = []
    if request.user.is_authenticated:
        currentUser = User.objects.get(id=request.user.id)
        likes = currentUser.userLikes.all()
    context = {
        'posts': postList,
        'title': 'Home',
        'likes': likes,
        'comments': comments
    }
    return render(request, 'posts/home.html', context)

def about(request):
    path = pathRecords(request.path)
    return render(request, 'posts/about.html', {'title': 'About'})

@AuthRequiredMiddleware
def register(request):
    path = pathRecords(request.path)
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created. You can log in using your account now')
            return redirect('login') #OR LOGIN??
    else:
        form = UserRegisterForm()
    return render(request, 'posts/register.html', {'form': form,
                                                   'title': 'Join Pytagram'})

class Login(FormView):
    form_class = AuthenticationForm
    success_url = "/"

    def get_context_data(self, **kwargs):
        path = pathRecords(self.request.path)
        context = super(Login, self).get_context_data(**kwargs)
        context['title'] = 'Login'
        return context

    def form_valid(self, form):
        user = User.objects.get(username=form.cleaned_data["username"])
        login(self.request, user)
        messages.success(
            self.request,
            f'Welcome back,'
        )
        return super(Login, self).form_valid(form)


class Logout(TemplateView):
    template_name = 'posts/logout.html'

    def get_context_data(self, **kwargs):
        path = pathRecords(self.request.path)
        logout(self.request)
        context = super(Logout, self).get_context_data(**kwargs)
        context['object'] = 'Logged you out'
        context['title'] = 'Logout Successful'
        return context


class ViewProfile(TemplateView):
    template_name = "posts/profile.html"

    def get_context_data(self, **kwargs):
        path = pathRecords(self.request.path)
        context = super(ViewProfile, self).get_context_data(**kwargs)

        currentUser = User.objects.get(username=kwargs["username"])
        context['object'] = currentUser

        # -- PAGINATION START-- #
        posts = currentUser.post_set.all().order_by('-date_posted')
        page = self.request.GET.get('page', 1)
        paginator = Paginator(posts, 3)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        # -- PAGINATION END -- #
        likes = []
        if self.request.user.is_authenticated:
            currentUser = User.objects.get(id=self.request.user.id)
            likes = currentUser.userLikes.all()
        context['likes'] = likes
        context['posts'] = posts
        context['following'] = User.objects.get(id=currentUser.id).profile.following.all()
        context['title'] = str(currentUser.username) + '\'s Profile'
        return context


def profileUpdate(request):
    path = pathRecords(request.path)
    img1 = request.user.profile.image
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            img2 = p_form.cleaned_data["image"]
            if img1 != img2:
                #delete the old image from S3
                s3 = boto3.resource("s3")
                obj = s3.Object("django-demo-app-files", str(img1))
                obj.delete()
                #delete the old image from S3 - end
            messages.success(request, f'Your account has been updated,')
            return redirect('/profile/' + request.user.username)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'title': 'Update Profile'
    }
    return render(request, 'posts/profileupdate.html', context)


def followUser(request, *args, **kwargs):
    if not request.user.is_authenticated:
        messages.error(request,
                       f'You need to login to do that')
        return redirect('login')

    followUser = User.objects.get(username=kwargs["username"])
    currentUser = User.objects.get(id=request.user.id)
    if followUser == currentUser:
        messages.warning(request, f'You cannot follow or unfollow yourself,')
        return redirect('/profile/' + kwargs['username'])
    if followUser in currentUser.profile.following.all():
        currentUser.profile.following.remove(followUser)
    else:
        currentUser.profile.following.add(followUser)
    path = pathRecords(request.path)
    return redirect(path[0])


class CreatePost(FormView):
    AuthRequiredMiddleware
    template_name = "posts/createpost.html"
    form_class = PostForm
    success_url = "/"

    def form_valid(self, form):
        path = pathRecords(self.request.path)
        user = User.objects.get(
            id=self.request.user.id
        )
        Post.objects.create(
            user=user,
            image=form.cleaned_data['image'],
            description=form.cleaned_data['description']
        )
        return super(CreatePost, self).form_valid(form)


def viewPost(request, *args, **kwargs):
    path = pathRecords(request.path)
    post = Post.objects.get(pk=kwargs['pk'])
    postLikes = []
    if request.user in post.postLikes.all():
        postLikes.append(request.user)
    for item in post.postLikes.all():
        if item != request.user:
            postLikes.append(item)
    comments = Comment.objects.filter(post=post)
    user = request.user
    commentLink = "#comment"
    if not request.user.is_authenticated:
        commentLink = '/login/'

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                post=post,
                user=user,
                text=form.cleaned_data["text"]
            )
            return redirect(path[0])
    else:
        form = CommentForm()
    context = {
        'form': form,
        'object': post,
        'comments': comments,
        'commentLink': commentLink,
        'postLikes': postLikes
    }
    return render(request, 'posts/viewpost.html', context)


def likePost(request, *args, **kwargs):
    path = pathRecords(request.path)
    if not request.user.is_authenticated:
        messages.error(request,
                         f'You need to login to do that!')
        return redirect('login')
    post = Post.objects.get(pk=kwargs["pk"])
    currentUser = User.objects.get(id=request.user.id)

    if currentUser in post.postLikes.all():
        post.postLikes.remove(currentUser)
    else:
        post.postLikes.add(currentUser)
        if post.user == currentUser:
            messages.success(request,
                             f'You liked your own photo; how about that')
    return redirect(path[0])


def postUpdate(request, *args, **kwargs):
    path = pathRecords(request.path)
    post = Post.objects.get(pk=kwargs['pk'])
    form = PostUpdateForm(instance=post)
    if not request.user.is_authenticated:
        messages.error(
            request,
            f'You need to login to your account first'
        )
        return redirect('login')
    else:
        if request.user.username == post.user.username:
            if request.method == 'POST':
                form = PostUpdateForm(request.POST,
                                      request.FILES,
                                      instance=post
                                      )
                if form.is_valid():
                    form.save()
                    messages.success(request, f'Your post has been updated,')
                    return redirect('/post/' + str(post.pk))
            else:
                form = PostUpdateForm(instance=post)
        else:
            messages.error(
                request,
                f'You don\'t have permission to do that,'
            )
            return redirect('/')
    context = {
        'form': form,
        'title': 'Update Post'
    }
    return render(request, 'posts/post_form.html', context)

def postDeleteForm(request, *args, **kwargs):
    post = Post.objects.get(pk=kwargs['pk'])
    if not request.user.is_authenticated:
        messages.error(
            request,
            f'Wanna login first?'
        )
        return redirect('login')
    if request.user.is_authenticated:
        if post.user != request.user:
            messages.error(
                request,
                f'You don\'t have permission to do that'
            )
            return redirect('/')

    if request.method == 'POST':
        form = PostDeleteForm(request.POST, instance=post)

        if form.is_valid():
            #DELETE FROM AWS S3
            s3 = boto3.resource("s3")
            obj = s3.Object("django-demo-app-files", str(post.image))
            obj.delete()
            # DELETE FROM AWS S3 - END
            post.delete()
            messages.success(
                request,
                f'Your post has been deleted,'
            )
            return redirect('home')
    else:
        form = PostDeleteForm(instance=post)
    context = {
        'post': post,
        'title': 'Confirm Deletion',
    }
    return render(request, 'posts/postdelete.html', context)


def commentUpdate(request, *args, **kwargs):
    path = pathRecords(request.path)
    comment = Comment.objects.get(pk=kwargs['pk'])
    form = CommentUpdateForm(instance=comment)

    if not request.user.is_authenticated:
        messages.error(
            request,
            f'You need to login to your account first'
        )
        return redirect('login')
    else:
        if request.user.username == comment.user.username:
            if request.method == 'POST':
                form = CommentUpdateForm(request.POST,
                                      instance=comment)
                if form.is_valid():
                    form.save()
                    messages.success(request, f'Your comment has been updated,')
                    return redirect('/post/' + str(comment.post.id) + '/#comment' + str(comment.id))
            else:
                form = CommentUpdateForm(instance=comment)
        else:
            messages.error(
                request,
                f'You don\'t have permission to do that,'
            )
            return redirect('/')
    context = {
        'form': form,
        'title': 'Update Comment'
    }
    return render(request, 'posts/comment_form.html', context)


def commentDelete(request, *args, **kwargs):
    comment = Comment.objects.get(pk=kwargs['pk'])
    if not request.user.is_authenticated:
        messages.error(
            request,
            f'Wanna login first?'
        )
        return redirect('login')
    if request.user.is_authenticated:
        if comment.user != request.user:
            messages.error(
                request,
                f'You don\'t have permission to do that'
            )
            return redirect('/')
    if request.method == 'POST':
        form = CommentDeleteForm(request.POST, instance=comment)

        if form.is_valid():
            comment.delete()
            messages.success(
                request,
                f'Your comment has been deleted,'
            )
            return redirect('home')
    else:
        form = CommentDeleteForm(instance=comment)

    context = {
        'form': form,
        'comment': comment,
        'title': 'Confirm Deletion',
    }
    return render(request, 'posts/commentdelete.html', context)

