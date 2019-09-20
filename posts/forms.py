from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post
from .models import Profile, CustomUser, Post, Comment

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'job', 'avatar', 'bio']

class PostForm(forms.Form):
    image = forms.ImageField()
    description = forms.CharField(max_length=300, required=False)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]

class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['description']

class CommentUpdateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class PostDeleteForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = []

class CommentDeleteForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = []