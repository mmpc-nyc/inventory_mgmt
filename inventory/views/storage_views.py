from django.views.generic import DetailView, ListView, UpdateView, DeleteView

from inventory.models.inventory_models import Storage, Item


class StorageList(ListView):
    model = Storage
    template_name_suffix = '_list'
    extra_context = {'title': 'Storage List'}


class StorageDetail(DetailView):
    model = Storage
    template_name_suffix = '_detail'
    extra_context = {'title': 'Storage Detail'}


class ItemList(ListView):
    model = Item
    template_name_suffix = '_list'
    extra_context = {'title': 'Item List'}


class ItemDetail(DetailView):
    model = Item
    template_name_suffix = '_detail'
    extra_context = {'title': 'Item Detail'}