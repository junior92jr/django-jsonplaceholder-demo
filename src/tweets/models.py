from django.db import models
from django.conf import settings

from common.models import BaseAppModel


class Post(BaseAppModel):
    """Model that represents Posts in the database."""

    external_id = models.IntegerField(unique=True)
    user_id = models.IntegerField()
    title = models.TextField()
    body = models.TextField()

    def __str__(self) -> str:
        return f"Post - {self.id}"


class Comment(BaseAppModel):
    """Model that represents Comment in the database."""

    external_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=240)
    email = models.EmailField(max_length=254, unique=True)
    body = models.TextField()

    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Comment - {self.id}"
