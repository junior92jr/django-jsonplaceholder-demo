from typing import List

from common.transactions import BulkCreateManager, BulkUpdateManager

from ..models import Post, Comment


class PostBulkCreate(BulkCreateManager):
    """Bulk Create in blocks for Post model."""

    def __init__(self, chunk_size: int) -> None:
        """Constructor that init parent with child parameters."""

        super(PostBulkCreate, self).__init__(Post, chunk_size)


class PostBulkUpdate(BulkUpdateManager):
    """Bulk Update in blocks for Post model."""

    def __init__(self, fields_lookup: List[str], chunk_size: int) -> None:
        """Constructor that init parent with child parameters."""

        super(PostBulkUpdate, self).__init__(Post, chunk_size, fields_lookup)


class CommentBulkCreate(BulkCreateManager):
    """Bulk Create in blocks for Comment model."""

    def __init__(self, chunk_size: int) -> None:
        """Constructor that init parent with child parameters."""

        super(CommentBulkCreate, self).__init__(Comment, chunk_size)


class CommentBulkUpdate(BulkUpdateManager):
    """Bulk Update in blocks for Comment model."""

    def __init__(self, fields_lookup: List[str], chunk_size: int) -> None:
        """Constructor that init parent with child parameters."""

        super(CommentBulkUpdate, self).__init__(
            Comment, chunk_size, fields_lookup)
