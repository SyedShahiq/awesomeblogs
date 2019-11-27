from blog.models import Post
from .serializers import BlogSerializers
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response



class BlogViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = BlogSerializers