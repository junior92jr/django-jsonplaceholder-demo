from django.db import models


class BaseAppModel(models.Model):
    """
    Base model with timestamps and simple serialization.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]

    def as_field_dict(self, include: list[str] | None = None) -> dict:
        """
        Return a dict of model field values for comparison or serialization.
        By default includes all concrete fields except PK/timestamps.
        """
        fields = include or [
            f.name
            for f in self._meta.fields
            if f.name not in ("id", "created_at", "updated_at")
        ]
        return {f: getattr(self, f) for f in fields}
