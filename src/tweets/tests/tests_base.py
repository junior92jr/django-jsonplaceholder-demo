import json
from unittest import mock

from django.test import TestCase


class ImportTestCase(TestCase):

    def setUp(self):
        self.initial_count = 0
        self.post_total_items = 19
        self.comment_total_items = 95
        self.even_chunk_size = 100

    def get_posts_payload(self) -> dict:
        return json.load(open('tweets/tests/resources/mocks/posts.json'))

    def get_comments_payload(self) -> dict:
        return json.load(open('tweets/tests/resources/mocks/comments.json'))

    def get_updated_posts_payload(self) -> dict:
        return json.load(open(
            'tweets/tests/resources/mocks/updated_posts.json'))

    def get_updated_comments_payload(self) -> dict:
        return json.load(open(
            'tweets/tests/resources/mocks/updated_comments.json'))

    def get_invalid_posts_payload(self) -> dict:
        return "whatever"

    def get_invalid_comments_payload(self) -> dict:
        return "whatever"

    def _mock_response(
            self,
            status=200,
            content="content",
            json_data=None,
            raise_for_status=None):

        mock_response = mock.Mock()
        mock_response.raise_for_status = mock.Mock()
        if raise_for_status:
            mock_response.raise_for_status.side_effect = raise_for_status
        mock_response.status_code = status
        mock_response.content = content

        if json_data:
            mock_response.json = mock.Mock(
                return_value=json_data
            )
        return mock_response
