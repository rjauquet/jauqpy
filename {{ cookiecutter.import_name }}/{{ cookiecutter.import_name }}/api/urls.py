from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

api_info = openapi.Info(
    title='{{ cookiecutter.project_name }} API',
    default_version='v1',
    description='',
)

schema_view = get_schema_view(
    api_info, authentication_classes=[], permission_classes=[], public=True
)

# pylint: disable=invalid-name
urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('schema(?P<format>.json|.yaml)$', schema_view.without_ui()),
    path('schema', schema_view.with_ui()),
]
