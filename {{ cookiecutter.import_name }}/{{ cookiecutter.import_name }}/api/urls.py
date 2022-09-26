"""
{{ cookiecutter.project_name }} url routing
"""
from django.contrib import admin
from django.urls import include, path

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from {{ cookiecutter.import_name }}.base.views import health, webhook

urlpatterns = [
    path("admin/docs/", include("django.contrib.admindocs.urls")),
    path('admin/', admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("api/health/", health, name="health"),
    path("api/webhook/", webhook, name="webhook"),
]
