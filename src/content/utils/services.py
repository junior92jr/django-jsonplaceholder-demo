import logging
from typing import Dict, List

from common.services import FakeApiRequestsHandler

logger = logging.getLogger(__name__)


class PostApiClient(FakeApiRequestsHandler):
    """
    Handler to fetch posts from JSONPlaceholder.
    """

    def list_items(self) -> List[Dict]:
        """
        Retrieve all posts from the API.
        """
        return self._list_from_endpoint("posts")


class CommentApiClient(FakeApiRequestsHandler):
    """
    Handler to fetch comments from JSONPlaceholder.
    """

    def list_items(self) -> List[Dict]:
        """
        Retrieve all comments from the API.
        """
        return self._list_from_endpoint("comments")
