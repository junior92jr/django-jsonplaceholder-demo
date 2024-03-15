from django.db import models
from django.forms.models import model_to_dict


class BaseAppModel(models.Model):
    """Base Model that contains time logging to be used in all Models."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    @property
    def to_dict(self):
        return model_to_dict(
            self, fields=[field.name for field in self._meta.fields])
