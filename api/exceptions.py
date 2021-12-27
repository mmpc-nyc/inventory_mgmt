from functools import wraps

from rest_framework import status
from rest_framework.response import Response

from main.exceptions import BaseError


def exception_serializer(func):
    """Decorator for serializing Inventory related Exceptions"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except BaseError as e:
            return Response(data={'error': e.message}, status=status.HTTP_400_BAD_REQUEST)
        return result
    return wrapper