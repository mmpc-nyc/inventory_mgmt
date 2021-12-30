from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView
from inventory.models.customer import Customer


class CustomerDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Customer
    template_name_suffix = '_detail'
    extra_context = {'title': 'Customer Detail'}
    permission_required = {'any': ('inventory_view_customer',)}


class CustomerListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Customer
    template_name_suffix = '_list'
    extra_context = {'title': 'Customer List'}
    permission_required = {'any': ('inventory_view_customer',)}


class CustomerCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Customer
    template_name_suffix = '_create'
    permission_required = {'any': ('inventory_create_customer',)}


class CustomerDeleteView(PermissionRequiredMixin, CreateView, DeleteView):
    model = Customer
    template_name_suffix = '_delete'
    permission_required = {'any': ('inventory_delete_customer',)}


class CustomerUpdateView(PermissionRequiredMixin, CreateView, UpdateView):
    model = Customer
    template_name_suffix = '_update'
    permission_required = {'any': ('inventory_update_customer',)}
