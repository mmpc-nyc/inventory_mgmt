from django.http import HttpResponse
from django.views.generic import TemplateView, DetailView, ListView
from django.views import View
from django_filters.views import FilterView


class HTMXDetailView(DetailView):
    def get_template_names(self):
        names = super().get_template_names()
        if self.request.htmx:
            names = [name.replace('/', '/partials/') for name in names]
        return names

    def delete(self, request, *args, **kwargs):
        return HttpResponse("")

    def put(self, request, *args, **kwargs):
        print('triggered updated')
        return super().get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if request.htmx:
            print(request.htmx)
        return super().get(request, *args, **kwargs)


class HTMXListView(FilterView, ListView):
    def get_template_names(self):
        names = super().get_template_names()
        if self.request.htmx:
            names = [name.replace('/', '/partials/') for name in names]
        return names
