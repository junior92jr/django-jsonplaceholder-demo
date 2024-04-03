from typing import List, Dict

from common.importers import ObjectImporter
from common.mixins import ObjectDiffMixin

from ..models import Post, Comment

from .transactions import (
    PostBulkCreate,
    PostBulkUpdate,
    CommentBulkCreate,
    CommentBulkUpdate
)

from .import_validators import PostImportValidator, CommentImportValidator


class PostImporter(ObjectImporter, ObjectDiffMixin):
    """Class that implements Post import create and update."""

    def __init__(self, objects_to_insert: List[Dict],
                 bulk_create: PostBulkCreate,
                 bulk_update: PostBulkUpdate) -> None:
        """Constructor that init parent with child parameters."""

        super(PostImporter, self).__init__(
            Post,
            objects_to_insert,
            PostImportValidator,
            bulk_create,
            bulk_update,
        )

    def _process_insert(self, obj: Dict) -> Dict:
        """Process custom create for Posts objects."""

        obj['user_id'] = obj.pop('userId')
        obj['external_id'] = obj.pop('id')

        return obj

    def _process_update(self, obj: Dict) -> Dict:
        """Process custom update for Posts objects."""

        obj['user_id'] = obj.pop('userId')
        obj['external_id'] = obj.pop('id')

        post_in_db = Post.objects.filter(external_id=obj['external_id'])

        if post_in_db:
            post_in_db = post_in_db.first()
            obj['id'] = post_in_db.id

        if not self.get_difference(post_in_db.to_dict, obj):
            return {}
        return obj


class CommentImporter(ObjectImporter, ObjectDiffMixin):
    """Class that implements Comment import create and update."""

    def __init__(self, objects_to_insert: List[Dict],
                 bulk_create: CommentBulkCreate,
                 bulk_update: CommentBulkUpdate) -> None:
        """Constructor that init parent with child parameters."""

        super(CommentImporter, self).__init__(
            Comment,
            objects_to_insert,
            CommentImportValidator,
            bulk_create,
            bulk_update
        )

    def _process_insert(self, obj: Dict) -> Dict:
        """Process custom create for Comment objects."""

        obj['post'] = obj.pop('postId')
        related_post = Post.objects.filter(external_id=obj['post'])

        if not related_post.exists():
            return {}

        related_post = related_post.first()
        obj['post'] = related_post
        obj['external_id'] = obj.pop('id')

        return obj

    def _process_update(self, obj: Dict) -> Dict:
        """Process custom update for Comment objects."""

        obj['post'] = obj.pop('postId')
        related_post = Post.objects.filter(external_id=obj['post'])

        if related_post.exists():
            comment_in_db = self._model_class.objects.filter(
                external_id=obj['id']).first()
            obj['external_id'] = obj.pop('id')
            obj['id'] = comment_in_db.id
            if self.get_difference(comment_in_db.to_dict, obj):
                obj['post'] = related_post.first()
                return obj
        return {}
