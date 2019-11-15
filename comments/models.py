from django.db import models
from django.utils import timezone
from blog.models import Post
# Create your models here.
class Comment(models.Model):
	content = models.TextField()
	date_posted = models.DateTimeField(default = timezone.now)
	post = models.ForeignKey(Post, on_delete = models.CASCADE)
