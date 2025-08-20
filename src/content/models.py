from django.conf import settings
from django.db import models

from common.models import BaseAppModel


def default_user_id() -> int:
    """
    Return the default user ID.
    """
    return getattr(settings, "DEFAULT_EXTERNAL_USER_ID", 99999942)


class Post(BaseAppModel):
    """
    Represents a blog or forum post.

    Attributes:
        external_id (PositiveIntegerField): External identifier (e.g., from an API).
        user_id (PositiveIntegerField): The ID of the user who created the post.
        title (CharField): The title of the post (max 255 characters).
        body (TextField): The content/body of the post.
    """

    external_id = models.PositiveIntegerField(unique=True, blank=True, null=True)
    user_id = models.PositiveIntegerField(default=default_user_id)
    title = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self) -> str:
        """
        Return a string representation of the Post.
        """
        return f"Post({self.id}): {self.title[:30]}"


class Comment(BaseAppModel):
    """
    Represents a comment on a Post.

    Attributes:
        external_id (PositiveIntegerField): External identifier (e.g., from an API).
        name (CharField): The name of the commenter (max 255 characters).
        email (EmailField): The email address of the commenter.
        body (TextField): The content of the comment.
        post (ForeignKey): The related Post this comment belongs to.
    """

    external_id = models.PositiveIntegerField(unique=True, blank=True, null=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    body = models.TextField()

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")

    def __str__(self) -> str:
        """
        Return a string representation of the Comment.
        """
        return f"Comment({self.id}) by {self.email}"
