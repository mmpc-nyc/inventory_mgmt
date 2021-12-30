from django.db.models import Model
from django.http import HttpResponse
from django.views.generic import DetailView, ListView


class AxiosDetailView(DetailView):
    def get_template_names(self):
        names = super().get_template_names()
        if self.request.headers.get('X-Axios-Header'):
            names = [name.replace('/', '/partials/') for name in names]
        return names

    def delete(self, request, *args, **kwargs):
        obj: Model = self.get_object()
        response = HttpResponse(obj)
        obj.delete()
        return response

    def put(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class AxiosListView(ListView):
    def get_template_names(self):
        names = super().get_template_names()
        if self.request.headers.get('X-Axios-Header'):
            names = [name.replace('/', '/partials/') for name in names]
        return names
