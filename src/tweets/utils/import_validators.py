from rest_framework import serializers


class PostImportValidator(serializers.Serializer):
    """Validator for Post objects to Import."""

    userId = serializers.IntegerField()
    id = serializers.IntegerField()
    title = serializers.CharField()
    body = serializers.CharField()


class CommentImportValidator(serializers.Serializer):
    """Validator for Comment objects to Import."""

    postId = serializers.IntegerField()
    id = serializers.IntegerField()
    name = serializers.CharField()
    email = serializers.EmailField()
    body = serializers.CharField()
