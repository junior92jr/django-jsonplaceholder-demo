from rest_framework import routers

from .views import CommentViewSet, PostViewSet

router = routers.SimpleRouter()
router.register(r"posts", PostViewSet, basename="post")
router.register(r"comments", CommentViewSet, basename="comment")

urlpatterns = router.urls
