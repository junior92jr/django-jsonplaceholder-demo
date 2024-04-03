import logging

from tweets.utils.api_clients import CommentsRequestHandler
from tweets.utils.importers import CommentImporter
from tweets.utils.transactions import (
    CommentBulkCreate,
    CommentBulkUpdate,
)


logger = logging.getLogger(__name__)


def synchronize_comments_task() -> None:
    """Task that sync comments from the database."""

    comments_handler = CommentsRequestHandler()
    try:
        retrieved_comments = comments_handler.get_list_request()
        logger.info(
            f"{len(retrieved_comments)} 'Comments' fetched.")

    except Exception as error:
        logger.error(
            f'An error occurred when requesting data from API: {error}')
        raise error

    comment_bulk_create = CommentBulkCreate(chunk_size=100)
    comment_bulk_update = CommentBulkUpdate(
        fields_lookup=['name', 'email', 'body', 'post'], chunk_size=100)

    try:
        comment_importer = CommentImporter(
            objects_to_insert=retrieved_comments,
            bulk_create=comment_bulk_create,
            bulk_update=comment_bulk_update
        )

        comment_importer.synchronize_data()

        logger.info(
            f"{comment_bulk_create.total_inserted} 'Comment(s)' inserted.")

        logger.info(
            f"{comment_bulk_update.total_updated} 'Comment(s)' updated.")

    except Exception as error:
        logger.error(f"An error occurred when synchronizing 'Posts': {error}")
        raise error
