"""
Base queryset functionality for models
"""
from django.db.models import QuerySet
from django.utils import timezone


class BaseQuerySet(QuerySet):
    """
    Base QuerySet used by all models
    """

    # pylint: disable=missing-function-docstring
    def delete(self):
        return self.filter(deleted_at=None).update(deleted_at=timezone.now())

    # pylint: disable=missing-function-docstring
    def hard_delete(self):
        super().delete()
