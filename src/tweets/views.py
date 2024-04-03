from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import PostSerializer, CommentSerializer
from .models import Post, Comment


class PostViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """Model Viewset that handles CRUD for Post Model."""

    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by('external_id')
    permission_classes = (AllowAny,)

    lookup_field = 'external_id'
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('external_id', 'user_id',)


class CommentViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    """Model Viewset that handles CRUD for Comment Model."""

    serializer_class = CommentSerializer
    queryset = Comment.objects.all().order_by('external_id')
    permission_classes = (AllowAny,)

    lookup_field = 'external_id'
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('external_id', 'post',)
