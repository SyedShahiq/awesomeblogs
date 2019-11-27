from rest_framework import serializers
from blog.models import Post
from django.contrib.auth.models import User

class UserSerializers(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('id','username')

class BlogSerializers(serializers.HyperlinkedModelSerializer):
    author = UserSerializers()
    class Meta:
        model = Post
        fields = ('title','content','date_posted','author')