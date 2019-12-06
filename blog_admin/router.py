from blog.api.viewsets import BlogViewSet,CommentViewSet,ReplyViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('blogs', BlogViewSet, base_name='blogs')
router.register('comments',CommentViewSet,base_name='comments')
router.register('reply',ReplyViewSet,base_name='reply')