from unittest import mock
from unittest.mock import patch

from requests.exceptions import HTTPError

from ..tests.tests_base import ImportTestCase
from ..utils.api_clients import PostsRequestHandler, CommentsRequestHandler


class RequestTestCase(ImportTestCase):

    @patch('requests.get')
    def test_post_request_success(
            self, mockeck_posts_response: mock.Mock) -> None:

        mocked_response = self._mock_response(
            json_data=self.get_posts_payload())
        mockeck_posts_response.return_value = mocked_response

        posts_hanlder = PostsRequestHandler()
        retrieved_posts = posts_hanlder.get_list_request()

        self.assertEqual(type(retrieved_posts), list)
        self.assertEqual(len(retrieved_posts), self.post_total_items)
        self.assertEqual(retrieved_posts[0]['userId'], 1)
        self.assertEqual(retrieved_posts[0]['id'], 1)
        self.assertEqual(retrieved_posts[0]['title'], 'title 1')
        self.assertEqual(retrieved_posts[0]['body'], 'body 1')
        self.assertTrue(mocked_response.raise_for_status.called)

    @patch('requests.get')
    def test_post_request_fail(
            self, mockeck_posts_response: mock.Mock) -> None:

        mocked_response = self._mock_response(
            status=500, raise_for_status=HTTPError("Post Api is down"))
        mockeck_posts_response.return_value = mocked_response

        posts_hanlder = PostsRequestHandler()
        retrieved_posts = posts_hanlder.get_list_request()

        self.assertEqual(type(retrieved_posts), list)
        self.assertEqual(len(retrieved_posts), 0)
        self.assertTrue(mocked_response.raise_for_status.called)

    @patch('requests.get')
    def test_comment_request_success(
            self, mockeck_comments_response: mock.Mock) -> None:

        mocked_response = self._mock_response(
            json_data=self.get_comments_payload())
        mockeck_comments_response.return_value = mocked_response

        comments_hanlder = CommentsRequestHandler()
        retrieved_comments = comments_hanlder.get_list_request()

        self.assertEqual(type(retrieved_comments), list)
        self.assertEqual(len(retrieved_comments), self.comment_total_items)
        self.assertEqual(retrieved_comments[0]['postId'], 1)
        self.assertEqual(retrieved_comments[0]['id'], 1)
        self.assertEqual(retrieved_comments[0]['name'], 'name 1')
        self.assertEqual(retrieved_comments[0]['email'], 'name1@mail.com')
        self.assertEqual(retrieved_comments[0]['body'], 'body 1')
        self.assertTrue(mocked_response.raise_for_status.called)

    @patch('requests.get')
    def test_comment_request_fail(
            self, mockeck_comments_response: mock.Mock) -> None:

        mocked_response = self._mock_response(
            status=500, raise_for_status=HTTPError("Comment Api is down"))
        mockeck_comments_response.return_value = mocked_response

        posts_hanlder = PostsRequestHandler()
        retrieved_posts = posts_hanlder.get_list_request()

        self.assertEqual(type(retrieved_posts), list)
        self.assertEqual(len(retrieved_posts), 0)
        self.assertTrue(mocked_response.raise_for_status.called)
