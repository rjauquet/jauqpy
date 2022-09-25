"""
Django Views
"""
# pylint: disable=unused-argument
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(http_method_names=["POST"])
def webhook(request):
    """
    Handles incoming webhooks from configured external APIs
    """
    return Response(dict(status="OK"))


@api_view(http_method_names=["GET"])
def health(request):
    """
    Handles incoming webhooks from configured external APIs
    """
    return Response(dict(status="OK"))


