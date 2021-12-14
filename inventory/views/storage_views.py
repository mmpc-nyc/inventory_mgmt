from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView
from inventory.models import Storage


class StorageDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Storage
    template_name_suffix = '_detail'
    extra_context = {'title': 'Storage Detail'}
    permission_required = {'any': 'inventory_view_storage'}


class StorageListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Storage
    template_name_suffix = '_list'
    extra_context = {'title': 'Storage List'}
    permission_required = {'any': 'inventory_view_storage'}


class StorageCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Storage
    template_name_suffix = '_create'
    permission_required = {'any': ('storage_create_storage',)}


class StorageDeleteView(PermissionRequiredMixin, CreateView, DeleteView):
    model = Storage
    template_name_suffix = '_delete'
    permission_required = {'any': ('inventory_delete_storage',)}


class StorageUpdateView(PermissionRequiredMixin, CreateView, UpdateView):
    model = Storage
    template_name_suffix = '_update'
    permission_required = {'any': ('inventory_update_storage',)}

