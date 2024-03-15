import logging

from posts.utils.api_clients import PostsRequestHandler
from posts.utils.importers import PostImporter
from posts.utils.transactions import (
    PostBulkCreate,
    PostBulkUpdate
)


logger = logging.getLogger(__name__)


def syncronize_posts_task() -> None:
    """Task that sync posts from the database."""

    posts_hanlder = PostsRequestHandler()

    try:
        retrieved_posts = posts_hanlder.get_list_request()

        logger.info(f"{len(retrieved_posts)} 'Posts' fetched.")

    except Exception as error:
        logger.error(
            f'An error occurred when requesting data from API: {error}')
        raise error

    post_bulk_create = PostBulkCreate(chunk_size=100)
    post_bulk_update = PostBulkUpdate(
        fields_lookup=['title', 'body'], chunk_size=100)

    try:
        post_importer = PostImporter(
            objects_to_insert=retrieved_posts,
            bulk_create=post_bulk_create,
            bulk_update=post_bulk_update
        )

        post_importer.syncronize_data()

        logger.info(f"{post_bulk_create.total_inserted} 'Post(s)' inserted.")

        logger.info(f"{post_bulk_update.total_updated} 'Post(s)' updated.")

    except Exception as error:
        logger.error(f"An error occurred when syncronizing 'Posts': {error}")
        raise error
