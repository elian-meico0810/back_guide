from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed
from .APIResponse import APIResponse


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if isinstance(exc, AuthenticationFailed):
        return APIResponse.error(message="El token es invalido o ha expirado.", status=401)
    return response
