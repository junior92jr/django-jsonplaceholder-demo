from common.synchronizers import BaseSyncService
from content.models import Comment, Post
from content.utils.services import CommentApiClient, PostApiClient


class PostSyncService(BaseSyncService):
    """
    Synchronize posts from an external API into the local database.
    """

    model = Post
    handler_class = PostApiClient

    def map_fields(self, item: dict) -> dict:
        """
        Map fields from the API response to the model fields.
        """
        return {
            "title": item.get("title", ""),
            "body": item.get("body", ""),
        }


class CommentSyncService(BaseSyncService):
    """
    Synchronize comments from an external API into the local database.
    """

    model = Comment
    handler_class = CommentApiClient

    def map_fields(self, item: dict) -> dict:
        """
        Map fields from the API response to the model fields.
        """
        post = None
        post_id = item.get("postId")
        if post_id:
            post = Post.objects.filter(external_id=post_id).first()

        return {
            "name": item.get("name", ""),
            "email": item.get("email", ""),
            "body": item.get("body", ""),
            "post": post,
        }


def synchronize_posts_task() -> None:
    """
    Synchronize posts from an external API into the local database.
    """
    PostSyncService().synchronize()


def synchronize_comments_task() -> None:
    """
    Synchronize comments from an external API into the local database.
    """
    CommentSyncService().synchronize()
