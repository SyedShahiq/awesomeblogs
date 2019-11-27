from blog.api.viewsets import BlogViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('blogs', BlogViewSet, base_name='blogs')