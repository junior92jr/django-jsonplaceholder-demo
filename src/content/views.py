from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Comment, Post
from .serializers import CommentSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    """
    CRUD for Posts, including synchronization with external API.
    """

    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by("external_id")
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["external_id", "user_id"]


class CommentViewSet(viewsets.ModelViewSet):
    """
    CRUD for Comments, including synchronization with external API.
    """

    serializer_class = CommentSerializer
    queryset = Comment.objects.all().order_by("external_id")
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["external_id", "post"]
