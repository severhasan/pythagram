from django.contrib.auth.models import User
from django.db import models
from PIL import Image
from django.urls import reverse

# Create your models here.

class CustomUser(User):
    following = models.ManyToManyField('CustomUser')
    bio = models.CharField(max_length=250, blank=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, related_name='followers')
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    job = models.CharField(blank=True, max_length=30)
    avatar = models.CharField(blank=True, max_length=500)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    #No more running because of integration of s3
    # def save(self, *args, **kwargs):
    #     super().save()
    #
    #     img = Image.open(self.image.path)
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='post_pics')
    postLikes = models.ManyToManyField(User, related_name='userLikes', blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    description = models.CharField(blank=True, max_length=300)

    def __str__(self):
        return ('post_id: ' + str(self.id) + ' | user: ' + str(self.user))

    def get_absolute_url(self):
        return reverse('view-post', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)



