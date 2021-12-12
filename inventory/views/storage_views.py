from django.views.generic import DetailView, ListView, UpdateView, DeleteView

from inventory.models.inventory_models import Storage


class StorageList(ListView):
    model = Storage
    template_name_suffix = '_list'


class StorageDetail(DetailView):
    model = Storage
    template_name_suffix = '_detail'
