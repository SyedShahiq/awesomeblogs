from blog.models import Post
from .serializers import BlogSerializers
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class BlogViewSet(viewsets.ModelViewSet):
    # queryset = Post.objects.all()
    # serializer_class = BlogSerializers

    def list(self, request):
        queryset = Post.objects.all()
        serializer = BlogSerializers(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Post.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = BlogSerializers(user)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def user_posts(self, request, pk=None):
        queryset = Post.objects.filter(author=pk).order_by('-id')
        serializer = BlogSerializers(queryset, many=True)
        return Response(serializer.data)