from rest_framework import serializers

from .models import Comment, Post


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for the Post model.

    Provides serialization/deserialization for Post instances,
    used for API responses and requests.
    """

    class Meta:
        model = Post
        fields = (
            "id",
            "external_id",
            "user_id",
            "title",
            "body",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "external_id",
            "user_id",
            "created_at",
            "updated_at",
        )


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.

    Provides serialization/deserialization for Comment instances,
    used for API responses and requests.
    """

    class Meta:
        model = Comment
        fields = (
            "id",
            "external_id",
            "post",
            "name",
            "email",
            "body",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "external_id",
            "created_at",
            "updated_at",
        )
