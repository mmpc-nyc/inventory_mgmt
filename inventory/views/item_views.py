from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView
from inventory.models import Item


class ItemDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Item
    template_name_suffix = '_detail'
    extra_context = {'title': 'Item Detail'}
    permission_required = {'any': ('inventory_view_item',)}


class ItemListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Item
    template_name_suffix = '_list'
    extra_context = {'title': 'Item List'}
    permission_required = {'any': ('inventory_view_item',)}


class ItemCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Item
    template_name_suffix = '_create'
    permission_required = {'any': ('inventory_create_item',)}


class ItemDeleteView(PermissionRequiredMixin, CreateView, DeleteView):
    model = Item
    template_name_suffix = '_delete'
    permission_required = {'any': ('inventory_delete_item',)}


class ItemUpdateView(PermissionRequiredMixin, CreateView, UpdateView):
    model = Item
    template_name_suffix = '_update'
    permission_required = {'any': ('inventory_update_item',)}
