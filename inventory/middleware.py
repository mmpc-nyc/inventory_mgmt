from typing import Callable
from urllib.parse import unquote
from django.http import HttpRequest, HttpResponse


class AxiosMiddleware:
    """Middleware for testing if axios headers are coming in
    TODO:  Remove This or improve on it.
    """
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        request.headers.get('X-Axios-Header')
        return self.get_response(request)
