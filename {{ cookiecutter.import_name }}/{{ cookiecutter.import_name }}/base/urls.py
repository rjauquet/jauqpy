from django.urls import path

from {{ cookiecutter.import_name }}.base import views

urlpatterns = [
    path("health/", views.health, name="health"),
    path("webhook/", views.webhook, name="webhook"),
]
