from unittest.mock import patch

import pytest

from content.models import Comment, Post
from content.utils.synchronizers import CommentSyncService, PostSyncService


@pytest.mark.django_db
class TestSyncServices:
    """
    Test PostSyncService and CommentSyncService using fixtures.
    """

    def test_synchronize_posts_creates_objects(self, posts_payload) -> None:
        """
        Test that PostSyncService inserts new posts using fixture.
        """
        service = PostSyncService()

        with patch.object(
            service.handler_class, "list_items", return_value=posts_payload
        ):
            service.synchronize()

        assert Post.objects.count() == len(posts_payload)

        posts_in_db = list(Post.objects.order_by("external_id"))
        for i, post in enumerate(posts_in_db):
            assert post.title == posts_payload[i]["title"]
            assert post.body == posts_payload[i]["body"]

    def test_synchronize_comments_creates_objects(
        self, posts, comments_payload
    ) -> None:
        """
        Test that CommentSyncService inserts new comments using fixture.
        """
        service = CommentSyncService()

        with patch.object(
            service.handler_class, "list_items", return_value=comments_payload
        ):
            service.synchronize()

        assert Comment.objects.count() == len(comments_payload)

        comments_in_db = list(Comment.objects.order_by("external_id"))
        for i, comment in enumerate(comments_in_db):
            assert comment.name == comments_payload[i]["name"]
            assert comment.email == comments_payload[i]["email"]
            assert comment.body == comments_payload[i]["body"]

            post_id = comments_payload[i].get("postId")
            if post_id:
                assert comment.post.external_id == post_id
