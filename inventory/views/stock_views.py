from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView
from inventory.models.stock import Stock


class StockDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Stock
    template_name_suffix = '_detail'
    extra_context = {'title': 'Stock Detail'}
    permission_required = {'any': 'inventory_view_inventory'}


class StockListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Stock
    template_name_suffix = '_list'
    extra_context = {'title': 'Stock List'}
    permission_required = {'any': 'inventory_view_inventory'}


class StockCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Stock
    template_name_suffix = '_create'
    permission_required = {'any': ('inventory_create_inventory',)}


class StockDeleteView(PermissionRequiredMixin, CreateView, DeleteView):
    model = Stock
    template_name_suffix = '_delete'
    permission_required = {'any': ('inventory_delete_inventory',)}


class StockUpdateView(PermissionRequiredMixin, CreateView, UpdateView):
    model = Stock
    template_name_suffix = '_update'
    permission_required = {'any': ('inventory_update_inventory',)}

