from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView
from inventory.models import InventoryItem


class InventoryItemDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = InventoryItem
    template_name_suffix = '_detail'
    extra_context = {'title': 'InventoryItem Detail'}
    permission_required = {'any': ('inventory_view_inventoryitem',)}


class InventoryItemListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = InventoryItem
    template_name_suffix = '_list'
    extra_context = {'title': 'InventoryItem List'}
    permission_required = {'any': ('inventory_view_inventoryitem',)}


class InventoryItemCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = InventoryItem
    template_name_suffix = '_create'
    permission_required = {'any': ('inventory_create_inventoryitem',)}


class InventoryItemDeleteView(PermissionRequiredMixin, CreateView, DeleteView):
    model = InventoryItem
    template_name_suffix = '_delete'
    permission_required = {'any': ('inventory_delete_inventoryitem',)}


class InventoryItemUpdateView(PermissionRequiredMixin, CreateView, UpdateView):
    model = InventoryItem
    template_name_suffix = '_update'
    permission_required = {'any': ('inventory_update_inventoryitem',)}
