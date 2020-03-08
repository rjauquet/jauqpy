"""
Django queryset managers for models.
"""
from django.db.models.manager import Manager

from {{ cookiecutter.import_name }}.base.querysets import BaseQuerySet


class BaseManager(Manager.from_queryset(BaseQuerySet)):  # type: ignore
    """
    A base manager for all models.

    This manager allows quick filtering of soft-deleted objects.
    """

    show_existing: bool = True
    show_deleted: bool = False

    def __init__(self, *args, show_existing=True, show_deleted=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.show_existing = show_existing
        self.show_deleted = show_deleted

    def get_queryset(self):
        """
        Extends the base `get_queryset` to optionally filter soft-deleted objects
        """
        base_queryset = super().get_queryset()
        queryset = base_queryset.none()
        if self.show_deleted:
            queryset |= base_queryset.filter(deleted_at__isnull=False)
        if self.show_existing:
            queryset |= base_queryset.filter(deleted_at__isnull=True)
        return queryset
