from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import PostSerializer, CommentSerializer
from .models import Post, Comment


class PostViewSet(viewsets.ModelViewSet):
    """Model Viewset that handles CRUD for Post Model."""

    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by('id')
    # permission_classes = (IsAuthenticated,)
    permission_classes = (AllowAny,)

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('external_id', 'user_id',)


class CommentViewSet(viewsets.ModelViewSet):
    """Model Viewset that handles CRUD for Comment Model."""

    serializer_class = CommentSerializer
    queryset = Comment.objects.all().order_by('id')
    # permission_classes = (IsAuthenticated,)
    permission_classes = (AllowAny,)

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('external_id', 'post',)
