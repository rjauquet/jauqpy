"""
Base admin tools for building consistent admin interfaces.
"""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


class SoftDeleteListFilter(admin.ListFilter):
    """
    Handles filtering of soft deleted objects

    see also:
    https://docs.djangoproject.com/en/3.0/topics/i18n/translation/#standard-translation
    https://code.djangoproject.com/ticket/8851
    """

    title = _('soft deleted')
    parameter_name = 'show'

    def __init__(self, request, params, model, model_admin):
        super().__init__(request, params, model, model_admin)
        if self.parameter_name in params:
            value = params.pop(self.parameter_name)
            self.used_parameters[self.parameter_name] = value

    # pylint: disable=missing-function-docstring
    def show_all(self):
        return self.used_parameters.get(self.parameter_name) == '__all__'

    # pylint: disable=missing-function-docstring
    def has_output(self):
        return True

    # pylint: disable=missing-function-docstring
    def choices(self, changelist):
        return [
            {
                'selected': self.show_all(),
                'query_string': changelist.get_query_string(
                    {self.parameter_name: '__all__'}
                ),
                'display': _('show soft deleted'),
            },
            {
                'selected': not self.show_all(),
                'query_string': changelist.get_query_string(
                    remove=[self.parameter_name]
                ),
                'display': _('hide soft deleted'),
            },
        ]

    # pylint: disable=missing-function-docstring
    def expected_parameters(self):
        return [self.parameter_name]

    # pylint: disable=missing-function-docstring
    def queryset(self, request, queryset):
        if not self.show_all():
            return queryset.filter(deleted_at__isnull=True)
        return queryset


class BaseModelAdmin(admin.ModelAdmin):
    """
    Generic base admin overrides.
    """

    def get_queryset(self, request):
        """
        Shows soft deleted objects in admin querysets.
        """
        return self.model.all_objects.get_queryset()

    def get_readonly_fields(self, request, obj=None):
        """
        Sets generic timestamp data to readonly
        """
        fields = super().get_readonly_fields(request, obj)
        fields += ('deleted_at', 'created_at', 'updated_at')
        return fields

    def get_list_filter(self, request):
        """
        Adds soft delete filter to all pages. Defaults to hiding soft deleted.
        """
        list_filter = super().get_list_filter(request)
        list_filter += (SoftDeleteListFilter,)
        return list_filter
