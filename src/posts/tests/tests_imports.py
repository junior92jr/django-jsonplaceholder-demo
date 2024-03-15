from unittest import mock

from django.db import DatabaseError

from ..tests.tests_base import ImportTestCase
from ..models import Post, Comment
from ..utils.importers import PostImporter, CommentImporter
from ..utils.transactions import (
    PostBulkCreate,
    PostBulkUpdate,
    CommentBulkCreate,
    CommentBulkUpdate,
)


class SynchronizerTestCase(ImportTestCase):

    def set_post_synchronize_data(self, retrieved_posts: dict) -> None:

        post_bulk_create = PostBulkCreate(chunk_size=self.even_chunk_size)
        post_bulk_update = PostBulkUpdate(
            chunk_size=self.even_chunk_size, fields_lookup=['title', 'body'])

        post_importer = PostImporter(
                objects_to_insert=retrieved_posts,
                bulk_create=post_bulk_create,
                bulk_update=post_bulk_update
        )

        post_importer.synchronize_data()

    def set_comments_synchronize_data(self, retrieved_comments: dict) -> None:

        comment_bulk_create = CommentBulkCreate(
            chunk_size=self.even_chunk_size)
        comment_bulk_update = CommentBulkUpdate(
            chunk_size=self.even_chunk_size,
            fields_lookup=['name', 'email', 'body', 'post']
        )

        comment_importer = CommentImporter(
            objects_to_insert=retrieved_comments,
            bulk_create=comment_bulk_create,
            bulk_update=comment_bulk_update
        )

        comment_importer.synchronize_data()

    def test_import_posts_success(self) -> None:

        self.assertEqual(Post.objects.all().count(), self.initial_count)

        retrieved_posts = self.get_posts_payload()
        self.set_post_synchronize_data(retrieved_posts)

        posts_examples = Post.objects.all()
        self.assertEqual(posts_examples[0].user_id, 1)
        self.assertEqual(posts_examples[0].external_id, 1)
        self.assertEqual(posts_examples[0].title, 'title 1')
        self.assertEqual(posts_examples[0].body, 'body 1')

        self.assertEqual(posts_examples[1].user_id, 1)
        self.assertEqual(posts_examples[1].external_id, 2)
        self.assertEqual(posts_examples[1].title, 'title 2')
        self.assertEqual(posts_examples[1].body, 'body 2')

        self.assertEqual(Post.objects.all().count(), self.post_total_items)

    def test_update_posts_success(self) -> None:

        self.assertEqual(Post.objects.all().count(), self.initial_count)
        self.test_import_posts_success()

        posts_examples = Post.objects.all()
        self.assertEqual(posts_examples[0].user_id, 1)
        self.assertEqual(posts_examples[0].external_id, 1)
        self.assertEqual(posts_examples[0].title, 'title 1')
        self.assertEqual(posts_examples[0].body, 'body 1')

        self.assertEqual(posts_examples[1].user_id, 1)
        self.assertEqual(posts_examples[1].external_id, 2)
        self.assertEqual(posts_examples[1].title, 'title 2')
        self.assertEqual(posts_examples[1].body, 'body 2')

        retrieved_posts = self.get_updated_posts_payload()
        self.set_post_synchronize_data(retrieved_posts)

        posts_examples = Post.objects.all()
        self.assertEqual(posts_examples[0].user_id, 1)
        self.assertEqual(posts_examples[0].external_id, 1)
        self.assertEqual(posts_examples[0].title, 'updated title 1')
        self.assertEqual(posts_examples[0].body, 'updated body 1')

        self.assertEqual(posts_examples[1].user_id, 1)
        self.assertEqual(posts_examples[1].external_id, 2)
        self.assertEqual(posts_examples[1].title, 'updated title 2')
        self.assertEqual(posts_examples[1].body, 'updated body 2')

        self.assertEqual(Post.objects.all().count(), self.post_total_items)

    def test_posts_invalid_payload(self) -> None:

        with self.assertRaises(ValueError) as catched_exception:

            retrieved_posts = self.get_invalid_posts_payload()
            self.set_post_synchronize_data(retrieved_posts)

        self.assertEqual(ValueError, type(catched_exception.exception))
        self.assertEqual(Post.objects.all().count(), self.initial_count)

    def test_comments_without_posts_success(self) -> None:

        self.assertEqual(Comment.objects.all().count(), self.initial_count)

        retrieved_comments = self.get_comments_payload()
        self.set_comments_synchronize_data(retrieved_comments)

        self.assertEqual(Comment.objects.all().count(), self.initial_count)

    def test_comments_with_posts_success(self) -> None:

        self.assertEqual(Comment.objects.all().count(), self.initial_count)

        self.test_import_posts_success()

        self.assertEqual(Post.objects.all().count(), self.post_total_items)

        retrieved_comments = self.get_comments_payload()
        self.set_comments_synchronize_data(retrieved_comments)

        self.assertEqual(
            Comment.objects.all().count(), self.comment_total_items)

        comment_examples = Comment.objects.all()
        self.assertEqual(comment_examples[0].post.id, 1)
        self.assertEqual(comment_examples[0].external_id, 1)
        self.assertEqual(comment_examples[0].name, 'name 1')
        self.assertEqual(comment_examples[0].email, 'name1@mail.com')
        self.assertEqual(comment_examples[0].body, 'body 1')

        self.assertEqual(comment_examples[1].post.id, 1)
        self.assertEqual(comment_examples[1].external_id, 2)
        self.assertEqual(comment_examples[1].name, 'name 2')
        self.assertEqual(comment_examples[1].email, 'name2@mail.com')
        self.assertEqual(comment_examples[1].body, 'body 2')

    def test_update_comments_success(self) -> None:

        self.assertEqual(Comment.objects.all().count(), self.initial_count)

        self.test_comments_with_posts_success()

        comment_examples = Comment.objects.all()
        self.assertEqual(comment_examples[0].post.id, 1)
        self.assertEqual(comment_examples[0].external_id, 1)
        self.assertEqual(comment_examples[0].name, 'name 1')
        self.assertEqual(comment_examples[0].email, 'name1@mail.com')
        self.assertEqual(comment_examples[0].body, 'body 1')

        self.assertEqual(comment_examples[1].post.id, 1)
        self.assertEqual(comment_examples[1].external_id, 2)
        self.assertEqual(comment_examples[1].name, 'name 2')
        self.assertEqual(comment_examples[1].email, 'name2@mail.com')
        self.assertEqual(comment_examples[1].body, 'body 2')

        retrieved_comments = self.get_updated_comments_payload()
        self.set_comments_synchronize_data(retrieved_comments)

        comment_examples = Comment.objects.all()
        self.assertEqual(comment_examples[0].post.id, 1)
        self.assertEqual(comment_examples[0].external_id, 1)
        self.assertEqual(comment_examples[0].name, 'updated name 1')
        self.assertEqual(comment_examples[0].email, 'updatedname1@mail.com')
        self.assertEqual(comment_examples[0].body, 'updated body 1')

        self.assertEqual(comment_examples[1].post.id, 1)
        self.assertEqual(comment_examples[1].external_id, 2)
        self.assertEqual(comment_examples[1].name, 'updated name 2')
        self.assertEqual(comment_examples[1].email, 'updatedname2@mail.com')
        self.assertEqual(comment_examples[1].body, 'updated body 2')

    def test_comments_invalid_payload(self) -> None:

        with self.assertRaises(ValueError) as catched_exception:

            retrieved_comments = self.get_invalid_comments_payload()
            self.set_comments_synchronize_data(retrieved_comments)

        self.assertEqual(ValueError, type(catched_exception.exception))
        self.assertEqual(Comment.objects.all().count(), self.initial_count)


class BulkTransactionTestCase(SynchronizerTestCase):

    def test_post_bulk_create_transaction_rollback(self) -> None:

        with self.assertRaises(DatabaseError) as catched_exception:
            with mock.patch.object(PostBulkCreate, '_commit') as mocked_commit:
                mocked_commit.side_effect = DatabaseError(
                    "Mock Database Error")

                self.test_import_posts_success()

        self.assertEqual(DatabaseError, type(catched_exception.exception))
        self.assertEqual(Post.objects.all().count(), self.initial_count)

    def test_post_bulk_update_transaction_rollback(self) -> None:
        with self.assertRaises(DatabaseError) as catched_exception:
            with mock.patch.object(PostBulkUpdate, '_commit') as mocked_commit:
                mocked_commit.side_effect = DatabaseError(
                    "Mock Database Error")

                self.test_update_posts_success()

        self.assertEqual(DatabaseError, type(catched_exception.exception))
        self.assertEqual(Post.objects.all().count(), self.post_total_items)

    def test_comment_bulk_create_transaction_rollback(self) -> None:
        with self.assertRaises(DatabaseError) as catched_exception:
            with mock.patch.object(
                    CommentBulkCreate, '_commit') as mocked_commit:
                mocked_commit.side_effect = DatabaseError(
                    "Mock Database Error")

                self.test_comments_with_posts_success()
        self.assertEqual(DatabaseError, type(catched_exception.exception))
        self.assertEqual(Comment.objects.all().count(), self.initial_count)

    def test_comment_bulk_update_transaction_rollback(self) -> None:
        with self.assertRaises(DatabaseError) as catched_exception:
            with mock.patch.object(
                    CommentBulkUpdate, '_commit') as mocked_commit:
                mocked_commit.side_effect = DatabaseError(
                    "Mock Database Error")

                self.test_update_comments_success()
        self.assertEqual(DatabaseError, type(catched_exception.exception))
        self.assertEqual(
            Comment.objects.all().count(), self.comment_total_items)
