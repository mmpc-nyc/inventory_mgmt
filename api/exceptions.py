from functools import wraps
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response


def exception_serializer(func):
    """Decorator for serializing Inventory related Exceptions"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except ValidationError as e:
            return Response(data={'error': e.message}, status=status.HTTP_400_BAD_REQUEST)
        return result

    return wrapper
