from rest_framework import routers

from .views import PostViewSet, CommentViewSet


router = routers.SimpleRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = router.urls
