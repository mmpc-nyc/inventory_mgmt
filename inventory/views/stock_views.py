from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView
from inventory.models import Stock


class InventoryDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Stock
    template_name_suffix = '_detail'
    extra_context = {'title': 'Inventory Detail'}
    permission_required = {'any': 'inventory_view_inventory'}


class InventoryListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Stock
    template_name_suffix = '_list'
    extra_context = {'title': 'Inventory List'}
    permission_required = {'any': 'inventory_view_inventory'}


class InventoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Stock
    template_name_suffix = '_create'
    permission_required = {'any': ('inventory_create_inventory',)}


class InventoryDeleteView(PermissionRequiredMixin, CreateView, DeleteView):
    model = Stock
    template_name_suffix = '_delete'
    permission_required = {'any': ('inventory_delete_inventory',)}


class InventoryUpdateView(PermissionRequiredMixin, CreateView, UpdateView):
    model = Stock
    template_name_suffix = '_update'
    permission_required = {'any': ('inventory_update_inventory',)}

