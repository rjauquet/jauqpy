# type: ignore
"""
Base admin tools for building consistent admin interfaces.
"""
# pylint: disable=missing-function-docstring
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

READ = 4


class SoftDeleteListFilter(admin.ListFilter):
    """
    Handles filtering of soft deleted objects

    see also:
    https://docs.djangoproject.com/en/3.0/topics/i18n/translation/#standard-translation
    https://code.djangoproject.com/ticket/8851
    """

    title = _("soft deleted")
    parameter_name = "show"

    def __init__(self, request, params, model, model_admin):
        super().__init__(request, params, model, model_admin)
        if self.parameter_name in params:
            value = params.pop(self.parameter_name)
            self.used_parameters[self.parameter_name] = value

    # pylint: disable=missing-function-docstring
    def show_all(self):
        return self.used_parameters.get(self.parameter_name) == "__all__"

    # pylint: disable=missing-function-docstring
    def has_output(self):
        return True

    # pylint: disable=missing-function-docstring
    def choices(self, changelist):
        return [
            {
                "selected": self.show_all(),
                "query_string": changelist.get_query_string(
                    {self.parameter_name: "__all__"}
                ),
                "display": _("show soft deleted"),
            },
            {
                "selected": not self.show_all(),
                "query_string": changelist.get_query_string(
                    remove=[self.parameter_name]
                ),
                "display": _("hide soft deleted"),
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


class BaseInlineAdmin(admin.TabularInline):
    """
    Defaults for read-only inline models
    """

    extra = 0
    log_get_requests = False

    def get_fieldsets(self, request, obj=None):
        # log whenever the fields are loaded if the model is set to log reads
        if obj and self.log_get_requests and request.user:
            content_type_id = ContentType.objects.get_for_model(self.model).id
            LogEntry.objects.log_action(
                request.user.id,
                content_type_id,
                obj.id,
                str(obj),
                READ,
                change_message="Viewed",
            )
        return super().get_fieldsets(request, obj=obj)

    def has_change_permission(self, request, obj=None):
        return False

    def id_link(self, obj):
        url = obj.get_admin_url()
        return format_html("<a href='{url}'>{id}</a>", url=url, id=str(obj.id))

    id_link.short_description = "ID"  # type: ignore

    def natural_id_link(self, obj):
        url = obj.get_admin_url()
        return format_html("<a href='{url}'>{id}</a>", url=url, id=str(obj.natural_id))

    natural_id_link.short_description = "Short ID"  # type: ignore


class BaseModelAdmin(admin.ModelAdmin):
    """
    Generic base admin overrides.
    """

    log_get_requests = False

    def get_search_fields(self, request):
        """
        Defaults to allowing ID searches
        """
        return ["id"]

    def get_queryset(self, request):
        """
        Shows soft deleted objects in admin querysets.
        """
        return self.model.all_objects.get_queryset()

    def get_fieldsets(self, request, obj=None):
        """
        Organizes defaults into CRUD fieldset
        """
        # log whenever the fields are loaded if the model is set to log reads
        if obj and self.log_get_requests and request.user:
            content_type_id = ContentType.objects.get_for_model(self.model).id
            LogEntry.objects.log_action(
                request.user.id,
                content_type_id,
                obj.id,
                str(obj),
                READ,
                change_message="Viewed",
            )

        dates_fieldset = (
            "Dates",
            {"fields": ("deleted_at", "created_at", "updated_at")},
        )

        return (dates_fieldset,)

    def get_readonly_fields(self, request, obj=None):
        """
        Sets generic timestamp data to readonly
        """
        fields = super().get_readonly_fields(request, obj=obj)
        fields += ("deleted_at", "created_at", "updated_at")
        return fields

    def get_list_filter(self, request):
        """
        Adds soft delete filter to all pages. Defaults to hiding soft deleted.
        """
        list_filter = super().get_list_filter(request)
        list_filter += (SoftDeleteListFilter,)
        return list_filter

    def id_link(self, obj):
        url = obj.get_admin_url()
        return format_html("<a href='{url}'>{id}</a>", url=url, id=str(obj.id))

    id_link.short_description = "ID"  # type: ignore

    def natural_id_link(self, obj):
        url = obj.get_admin_url()
        return format_html("<a href='{url}'>{id}</a>", url=url, id=str(obj.natural_id))

    natural_id_link.short_description = "Short ID"  # type: ignore
