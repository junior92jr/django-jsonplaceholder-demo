from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth import get_user_model

from ..models import Post, Comment


class AuthVieSetTestCase(APITestCase):
    def setUp(self) -> None:

        self.user = get_user_model().objects.create_user(
            username='testuser', password='12345')

        self.client.force_authenticate(user=self.user)
        self.header = {}


class PostVieSetTestCase(AuthVieSetTestCase):

    def test_create_post_201(self) -> None:

        data = {
            'title': 'test title',
            'body': 'test body'
        }

        response = self.client.post(
            '/api/v1/posts/', data, **self.header, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(Post.objects.get().title, 'test title')
        self.assertEqual(Post.objects.get().body, 'test body')

    def test_create_post_400(self) -> None:

        data = {
            'title': '',
            'body': ''
        }

        response = self.client.post(
            '/api/v1/posts/', data, **self.header, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.all().count(), 0)

    def test_full_edit_post_200(self) -> None:

        self.test_create_post_201()

        data = {
            'title': 'updated test title',
            'body': 'test body'
        }

        response = self.client.put(
            '/api/v1/posts/1/', data, **self.header, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(Post.objects.get().title, 'updated test title')
        self.assertEqual(Post.objects.get().body, 'test body')

    def test_full_edit_post_404(self) -> None:

        data = {
            'title': 'updated test title',
            'body': 'test body'
        }

        response = self.client.put(
            '/api/v1/posts/1/', data, **self.header, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_edit_post_200(self) -> None:

        self.test_create_post_201()

        data = {
            'title': 'updated test title',
        }

        response = self.client.patch(
            '/api/v1/posts/1/', data, **self.header, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(Post.objects.get().title, 'updated test title')
        self.assertEqual(Post.objects.get().body, 'test body')

    def test_partial_edit_post_404(self) -> None:
        data = {
            'title': 'updated test title',
            'body': 'test body'
        }

        response = self.client.patch(
            '/api/v1/posts/1/', data, **self.header, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_all_post_200(self) -> None:

        self.test_create_post_201()

        response = self.client.get(
            '/api/v1/posts/', **self.header, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_response = response.json()

        self.assertTrue('count' in json_response)
        self.assertTrue('next' in json_response)
        self.assertTrue('previous' in json_response)
        self.assertTrue('results' in json_response)
        self.assertEqual(len(json_response['results']), 1)

    def test_retrieve_post_by_id_200(self) -> None:

        self.test_create_post_201()

        response = self.client.get(
            '/api/v1/posts/1/', **self.header, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_response = response.json()

        self.assertTrue('id' in json_response)
        self.assertTrue('external_id' in json_response)
        self.assertTrue('user_id' in json_response)
        self.assertTrue('title' in json_response)
        self.assertTrue('body' in json_response)
        self.assertTrue('created_at' in json_response)
        self.assertTrue('updated_at' in json_response)

    def test_retrieve_post_by_id_404(self) -> None:

        response = self.client.get(
            '/api/v1/posts/1/', **self.header, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_post_204(self) -> None:

        self.test_create_post_201()

        response = self.client.delete(
            '/api/v1/posts/1/', **self.header, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.all().count(), 0)

    def test_delete_post_404(self) -> None:

        response = self.client.delete(
            '/api/v1/posts/1/', **self.header, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CommentVieSetTestCase(PostVieSetTestCase):

    def test_create_comment_201(self) -> None:

        self.test_create_post_201()

        data = {
            'post': 1,
            'name': 'name 1',
            'email': 'email1@mail.com',
            'body': 'body 1'
        }

        response = self.client.post(
            '/api/v1/comments/', data, **self.header, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.all().count(), 1)
        self.assertEqual(Comment.objects.get().post.id, 1)
        self.assertEqual(Comment.objects.get().name, 'name 1')
        self.assertEqual(Comment.objects.get().email, 'email1@mail.com')
        self.assertEqual(Comment.objects.get().body, 'body 1')

    def test_create_comment_400(self) -> None:
        data = {
            'post': 'dasdasda',
            'name': 'name 1',
            'email': 'email1@mail.com',
            'body': 'body 1'
        }

        response = self.client.post(
            '/api/v1/comments/', data, **self.header, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.all().count(), 0)

    def test_full_edit_comment_200(self) -> None:

        self.test_create_comment_201()

        data = {
            'post': 1,
            'name': 'updated name 1',
            'email': 'email1@mail.com',
            'body': 'updated body 1'
        }

        response = self.client.put(
            '/api/v1/comments/1/', data, **self.header, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.all().count(), 1)
        self.assertEqual(Comment.objects.get().post.id, 1)
        self.assertEqual(Comment.objects.get().name, 'updated name 1')
        self.assertEqual(Comment.objects.get().email, 'email1@mail.com')
        self.assertEqual(Comment.objects.get().body, 'updated body 1')

    def test_full_edit_comment_404(self) -> None:

        data = {
            'post': 1,
            'name': 'updated name 1',
            'email': 'email1@mail.com',
            'body': 'updated body 1'
        }

        response = self.client.put(
            '/api/v1/comments/1/', data, **self.header, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_edit_comment_200(self) -> None:
        self.test_create_comment_201()

        data = {
            'name': 'updated name 1',
        }

        response = self.client.patch(
            '/api/v1/comments/1/', data, **self.header, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.all().count(), 1)
        self.assertEqual(Comment.objects.get().post.id, 1)
        self.assertEqual(Comment.objects.get().name, 'updated name 1')
        self.assertEqual(Comment.objects.get().email, 'email1@mail.com')
        self.assertEqual(Comment.objects.get().body, 'body 1')

    def test_partial_edit_comment_404(self) -> None:

        data = {
            'name': 'updated name 1',
        }

        response = self.client.patch(
            '/api/v1/comments/1/', data, **self.header, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_all_comment_200(self) -> None:
        self.test_create_comment_201()

        response = self.client.get(
            '/api/v1/comments/', **self.header, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_response = response.json()

        self.assertTrue('count' in json_response)
        self.assertTrue('next' in json_response)
        self.assertTrue('previous' in json_response)
        self.assertTrue('results' in json_response)
        self.assertEqual(len(json_response['results']), 1)

    def test_retrieve_comment_by_id_200(self) -> None:
        self.test_create_comment_201()

        response = self.client.get(
            '/api/v1/comments/1/', **self.header, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_response = response.json()

        self.assertTrue('id' in json_response)
        self.assertTrue('external_id' in json_response)
        self.assertTrue('post' in json_response)
        self.assertTrue('name' in json_response)
        self.assertTrue('email' in json_response)
        self.assertTrue('body' in json_response)
        self.assertTrue('created_at' in json_response)
        self.assertTrue('updated_at' in json_response)

    def test_retrieve_comment_by_id_404(self) -> None:

        response = self.client.get(
            '/api/v1/comments/1/', **self.header, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_comment_204(self) -> None:

        self.test_create_comment_201()
        response = self.client.delete(
            '/api/v1/comments/1/', **self.header, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_comment_404(self) -> None:

        response = self.client.delete(
            '/api/v1/comments/1/', **self.header, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
