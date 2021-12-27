from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView
from inventory.models import Order


class OrderDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Order
    template_name_suffix = '_detail'
    extra_context = {'title': 'Order Detail'}
    permission_required = {'any': ('inventory_view_order',)}


class OrderListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Order
    template_name_suffix = '_list'
    extra_context = {'title': 'Order List'}
    permission_required = {'any': ('inventory_view_order',)}


class OrderCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Order
    template_name_suffix = '_create'
    permission_required = {'any': ('inventory_create_order',)}


class OrderDeleteView(PermissionRequiredMixin, CreateView, DeleteView):
    model = Order
    template_name_suffix = '_delete'
    permission_required = {'any': ('inventory_delete_order',)}


class OrderUpdateView(PermissionRequiredMixin, CreateView, UpdateView):
    model = Order
    template_name_suffix = '_update'
    permission_required = {'any': ('inventory_update_order',)}
