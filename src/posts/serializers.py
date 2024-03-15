from rest_framework import serializers

from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    """Model Serializer used to visualize items from Event model."""

    class Meta:
        model = Post
        fields = (
            'id',
            'external_id',
            'user_id',
            'title',
            'body',
            'created_at',
            'updated_at',
        )

        read_only_fields = (
            'id',
            'external_id',
            'user_id',
            'created_at',
            'updated_at',
        )


class CommentSerializer(serializers.ModelSerializer):
    """Model Serializer used to visualize items from Event model."""

    class Meta:
        model = Comment
        fields = (
            'id',
            'external_id',
            'post',
            'name',
            'email',
            'body',
            'created_at',
            'updated_at',
        )

        read_only_fields = (
            'id',
            'external_id',
            'created_at',
            'updated_at',
        )
