from django.http import HttpResponse


def success(request, *args, **kwargs):
    response = HttpResponse(headers={'response': 'success'}, )
    return response
