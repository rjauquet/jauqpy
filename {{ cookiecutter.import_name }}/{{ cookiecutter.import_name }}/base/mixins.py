"""
Base model class for all models
"""
from django.db import models
from django.utils import timezone
from ulid2 import generate_ulid_as_uuid

from {{ cookiecutter.import_name }}.base.managers import BaseManager


class BaseModel(models.Model):
    """
    BaseModel for all models that adds soft deletion by default.
    """

    id = models.UUIDField(
        default=generate_ulid_as_uuid, primary_key=True, editable=False
    )
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = BaseManager()
    deleted_objects = BaseManager(show_existing=False, show_deleted=True)
    all_objects = BaseManager(show_deleted=True)
    _objects = models.Manager()

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.id)

    # pylint: disable=missing-function-docstring,unused-argument,arguments-differ
    def delete(self, *args, **kwargs):
        if not self.deleted_at:
            self.deleted_at = timezone.now()
            self.save()

    # pylint: disable=missing-function-docstring
    def hard_delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
