from functools import wraps

from rest_framework import status
from rest_framework.response import Response


class BaseError(Exception):
    """Exceptions related to inventory"""

    def __init__(self, message):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return f'{self.message}'


class JobStatusError(BaseError):
    """Error related to job status"""
    pass


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
