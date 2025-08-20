from typing import List

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from common.services import FakeApiRequestsHandler
from content.models import Comment, Post
from content.tests.payloads import COMMENTS_PAYLOAD, POSTS_PAYLOAD


@pytest.fixture
def api_client() -> APIClient:
    """
    Create a new APIClient instance for testing.
    """
    return APIClient()


@pytest.fixture
def user(db) -> User:
    """
    Create a new user for testing.
    """
    return User.objects.create_user(username="testuser", password="password")


@pytest.fixture
def auth_client(api_client, user) -> APIClient:
    """
    Create a new APIClient instance and authenticate it with the given user.
    """
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def posts(db, user) -> List[Post]:
    """
    Create a list of fake posts for testing.
    """
    return [
        Post.objects.create(
            external_id=i, user_id=user.id, title=f"Post {i}", body="Some body"
        )
        for i in range(1, 4)
    ]


@pytest.fixture
def comments(db, posts) -> List[Comment]:
    """
    Create a list of fake comments for testing.
    """
    return [
        Comment.objects.create(
            external_id=i,
            post=posts[0],
            name=f"Commenter {i}",
            email=f"user{i}@example.com",
            body="Comment body",
        )
        for i in range(1, 4)
    ]


@pytest.fixture
def posts_payload() -> List[dict]:
    """Return a list of fake post dictionaries."""
    return POSTS_PAYLOAD


@pytest.fixture
def comments_payload() -> List[dict]:
    """Return a list of fake comment dictionaries."""
    return COMMENTS_PAYLOAD


@pytest.fixture
def handler() -> FakeApiRequestsHandler:
    """
    Fixture that returns a fresh FakeApiRequestsHandler instance.
    """
    return FakeApiRequestsHandler()
