from unittest.mock import MagicMock, patch

import requests


class TestFakeApiRequestsHandler:
    """
    Unit tests for FakeApiRequestsHandler _list_from_endpoint method.
    """

    def test_list_from_endpoint_posts(self, handler, posts_payload):
        """
        _list_from_endpoint should return the posts payload.
        """
        mock_response = MagicMock()
        mock_response.json.return_value = posts_payload

        with patch.object(handler, "_fetch_request_data", return_value=mock_response):
            items = handler._list_from_endpoint("posts")
            assert items == posts_payload
            assert items[0]["title"].startswith("sunt aut facere")

    def test_list_from_endpoint_comments(self, handler, comments_payload):
        """
        _list_from_endpoint should return the comments payload.
        """
        mock_response = MagicMock()
        mock_response.json.return_value = comments_payload

        with patch.object(handler, "_fetch_request_data", return_value=mock_response):
            items = handler._list_from_endpoint("comments")
            assert items == comments_payload
            assert "email" in items[0]
            assert items[0]["email"] == "Eliseo@gardner.biz"

    def test_fetch_request_data_failure(self, handler, caplog):
        """
        Verify _fetch_request_data logs and returns None on error.
        """
        with patch.object(
            handler.session, "get", side_effect=requests.RequestException("boom")
        ):
            with caplog.at_level("ERROR"):
                response = handler._fetch_request_data(
                    "https://jsonplaceholder.typicode.com"
                )
            assert response is None
            assert (
                "API request to https://jsonplaceholder.typicode.com failed"
                in caplog.text
            )
