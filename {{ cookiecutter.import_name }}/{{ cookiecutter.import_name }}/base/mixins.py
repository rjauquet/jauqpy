"""
Base model class for all models
"""
from dataclasses import asdict, dataclass
from urllib.parse import urlencode

from django.db import models
from django.urls import reverse
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
        return str(self.natural_id)

    @property
    def short_id(self):
        """
        A base natural key of fixed length derived from the stringified ULID.
        """
        return str(self.id)[-6:]

    @property
    def natural_id(self):
        """
        A more human readable natural key including the model name.
        """
        return f"{self._meta.model_name}_{self.short_id}"

    # pylint: disable=unused-argument,arguments-differ
    def delete(self, *args, **kwargs):
        """
        Soft deletion override for the usual model delete method.
        """
        if not self.deleted_at:
            self.deleted_at = timezone.now()
            self.save()

    def hard_delete(self, *args, **kwargs):
        """
        Swaps in the original model delete method to a different name.
        """
        super().delete(*args, **kwargs)

    def get_admin_url(self):
        """
        Generates the change admin interface url for this model.
        """
        return reverse(
            f"admin:{self._meta.app_label}_{self._meta.model_name}_change",
            args=[self.id],
        )

    @classmethod
    def get_admin_list_url(cls, filters=None):
        """
        Generates the list admin interface url for this model.
        """
        filters = filters or {}
        return (
            reverse(
                f"admin:{cls._meta.app_label}_{cls._meta.model_name}_changelist",
            )
            + f"?{urlencode(filters)}"
        )


class PolymorficBaseModel(BaseModel):
    """
    Base model for polymorphic models
    """

    objects = PolymorphicBaseManager()
    deleted_objects = PolymorphicBaseManager(show_existing=False, show_deleted=True)
    all_objects = PolymorphicBaseManager(show_deleted=True)
    _objects = models.Manager()

    class Meta:
        abstract = True


@dataclass
class BaseDataClass:
    """
    Adds some helper methods for Cabinet dataclass based serializers
    """

    def to_dict(self):
        """
        Converts dataclass object to dictionary representation
        """
        return asdict(self)
