import ast
import json

from blog.models import Post,emotions
from comments.models import Comment,Reply
from .serializers import BlogSerializers,CommentSerializers,ReplySerializers,UserSerializers
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from blog.models import Post

class BlogViewSet(viewsets.ModelViewSet):
    # queryset = Post.objects.all()
    # serializer_class = BlogSerializers

    def list(self, request):
        queryset = Post.objects.all().order_by('-id')
        serializer = BlogSerializers(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        body = self.request.body
        body = ast.literal_eval(body.decode('utf-8'))
        title = body['title']
        content = body['content']
        author_id = body['author_id']
        post = Post.objects.create(title=title,content=content,author_id=author_id)
        print(post)
        return Response({"data":'This is ok'})

    def retrieve(self, request, pk=None):
        comments = Comment.objects.filter(post=pk).order_by('-id')
        comments_list = []
        for comment in comments:
            reply = Reply.objects.filter(comment=comment.id)
            reply_serializer = ReplySerializers(reply,many=True)
            thisdict = {
                "id": comment.id,
                "content": comment.content,
                "date_posted":comment.date_posted,
                "comment_author":{"id":comment.user_id,"username":comment.user.username},
                "reply":reply_serializer.data
                }
            comments_list.append(thisdict)
        emotion = emotions.objects.filter(post=pk).count()
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        serializer = BlogSerializers(post)
        post_obj = serializer.data
        post_obj.update({'likes':emotion})
        post_obj.update({"comments":comments_list})
        return Response(post_obj)

    @action(detail=True, methods=['get'])
    def user_posts(self, request, pk=None):
        queryset = Post.objects.filter(author=pk).order_by('-id')
        serializer = BlogSerializers(queryset, many=True)
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers

class ReplyViewSet(viewsets.ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializers
