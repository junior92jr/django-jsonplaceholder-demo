import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from content.models import Comment, Post


@pytest.mark.django_db
class TestPostAPI:
    """
    Tests for Post CRUD operations and filters.
    """

    def test_post_list(self, auth_client: APIClient, posts: list[Post]) -> None:
        """
        Retrieve a list of posts.
        """
        url = reverse("post-list")
        response = auth_client.get(url)
        assert response.status_code == 200
        assert len(response.data["results"]) == len(posts)

    def test_post_filter_by_external_id(
        self, auth_client: APIClient, posts: list[Post]
    ) -> None:
        """
        Filter posts by external_id.
        """
        url = reverse("post-list")
        response = auth_client.get(url, {"external_id": posts[0].external_id})
        assert response.status_code == 200
        assert len(response.data["results"]) == 1

    def test_post_create(self, auth_client: APIClient, user) -> None:
        """
        Create a new post.
        """
        url = reverse("post-list")
        data = {"user_id": user.id, "title": "New Post", "body": "New Body"}
        response = auth_client.post(url, data)
        assert response.status_code == 201
        assert Post.objects.filter(id=response.data["id"]).exists()

    def test_post_update(self, auth_client: APIClient, posts: list[Post]) -> None:
        """
        Update an existing post.
        """
        post = posts[0]
        url = reverse("post-detail", args=[post.id])
        data = {"title": "Updated Title", "body": "Updated Body"}
        response = auth_client.patch(url, data)
        assert response.status_code == 200
        post.refresh_from_db()
        assert post.title == "Updated Title"
        assert post.body == "Updated Body"

    def test_post_delete(self, auth_client: APIClient, posts: list[Post]) -> None:
        """
        Delete a post.
        """
        post = posts[0]
        url = reverse("post-detail", args=[post.id])
        response = auth_client.delete(url)
        assert response.status_code == 204
        assert not Post.objects.filter(id=post.id).exists()


@pytest.mark.django_db
class TestCommentAPI:
    """Tests for Comment CRUD operations and filters."""

    def test_comment_list(
        self, auth_client: APIClient, comments: list[Comment]
    ) -> None:
        """
        Retrieve a list of comments.
        """
        url = reverse("comment-list")
        response = auth_client.get(url)
        assert response.status_code == 200
        assert len(response.data["results"]) == len(comments)

    def test_comment_filter_by_post(
        self, auth_client: APIClient, posts: list[Post], comments: list[Comment]
    ) -> None:
        """
        Filter comments by associated post.
        """
        url = reverse("comment-list")
        response = auth_client.get(url, {"post": posts[0].id})
        assert response.status_code == 200
        for c in response.data["results"]:
            assert c["post"] == posts[0].id

    def test_comment_create(self, auth_client: APIClient, posts: list[Post]) -> None:
        """
        Create a new comment.
        """
        url = reverse("comment-list")
        data = {
            "external_id": 999,
            "post": posts[0].id,
            "name": "Test Commenter",
            "email": "test@example.com",
            "body": "Body",
        }
        response = auth_client.post(url, data)
        assert response.status_code == 201
        assert Comment.objects.filter(id=response.data["id"]).exists()

    def test_comment_update(
        self, auth_client: APIClient, comments: list[Comment]
    ) -> None:
        """
        Update an existing comment.
        """
        comment = comments[0]
        url = reverse("comment-detail", args=[comment.id])
        data = {"body": "Updated Comment Body"}
        response = auth_client.patch(url, data)
        assert response.status_code == 200
        comment.refresh_from_db()
        assert comment.body == "Updated Comment Body"

    def test_comment_delete(
        self, auth_client: APIClient, comments: list[Comment]
    ) -> None:
        """
        Delete a comment.
        """
        comment = comments[0]
        url = reverse("comment-detail", args=[comment.id])
        response = auth_client.delete(url)
        assert response.status_code == 204
        assert not Comment.objects.filter(id=comment.id).exists()


@pytest.mark.django_db
class TestPermissions:
    """
    Tests for API authentication and permission requirements.
    """

    def test_permission_required(self, api_client: APIClient) -> None:
        """
        Ensure unauthenticated users cannot access protected endpoints.
        """
        url = reverse("post-list")
        response = api_client.get(url)
        assert response.status_code == 403
