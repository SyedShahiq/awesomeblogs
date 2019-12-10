from rest_framework import serializers
from blog.models import Post
from comments.models import Comment,Reply
from django.contrib.auth.models import User


class UserSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class BlogSerializers(serializers.HyperlinkedModelSerializer):
    author = UserSerializers(read_only=True)
    author_id = serializers.IntegerField()

    class Meta:
        model = Post
        fields = ('id','title', 'content', 'date_posted', 'author_id', 'author')


class CommentSerializers(serializers.HyperlinkedModelSerializer):
    post_id = serializers.IntegerField()
    class Meta:
        model = Comment
        fields = ('id','content','post_id')

class ReplySerializers(serializers.HyperlinkedModelSerializer):
    user = UserSerializers(read_only=True)
    comment_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    class Meta:
        model = Reply
        fields = ('id','content','comment_id','user_id','user')