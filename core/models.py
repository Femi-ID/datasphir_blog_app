from django.db import models
from users.models import User
from django.conf import settings

class BlogPost(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts', on_delete=models.CASCADE)
    body = models.CharField(max_length=300)
    likes = models.IntegerField(default=0)


class Comments(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, related_name='post', on_delete=models.CASCADE)
    body = models.CharField(max_length=300)
    likes = models.IntegerField(default=0)



