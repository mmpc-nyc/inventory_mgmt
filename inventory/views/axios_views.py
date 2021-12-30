from django.http import HttpResponse
from django.views.generic import DetailView, ListView
from django_filters.views import FilterView


class HTMXDetailView(DetailView):
    def get_template_names(self):
        names = super().get_template_names()
        if self.request.headers.get('X-Axios-Header'):
            names = [name.replace('/', '/partials/') for name in names]
            print(names)
        return names

    def delete(self, request, *args, **kwargs):
        return HttpResponse("")

    def put(self, request, *args, **kwargs):
        print('triggered updated')
        return super().get(request, *args, **kwargs)


class HTMXListView(FilterView, ListView):
    def get_template_names(self):
        names = super().get_template_names()
        if self.request.htmx:
            names = [name.replace('/', '/partials/') for name in names]
        return names