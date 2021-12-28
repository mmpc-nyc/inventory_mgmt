from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, DeleteView, UpdateView

from inventory.models import GenericProduct
from inventory.views.mixins import HTMXDetailView, HTMXListView


class GenericProductDetailView(LoginRequiredMixin, PermissionRequiredMixin, HTMXDetailView):
    model = GenericProduct
    extra_context = {'title': 'GenericProduct Detail'}
    permission_required = {'any': ('inventory_view_genericproduct',)}


class GenericProductListView(LoginRequiredMixin, PermissionRequiredMixin, HTMXListView):
    model = GenericProduct
    paginate_by = 50
    template_name_suffix = '_list'
    extra_context = {'title': 'GenericProduct List'}
    permission_required = {'any': ('inventory_view_genericproduct',)}


class GenericProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = GenericProduct
    template_name_suffix = '_create'
    permission_required = {'any': ('inventory_create_genericproduct',)}


class GenericProductDeleteView(PermissionRequiredMixin, CreateView, DeleteView):
    model = GenericProduct
    template_name_suffix = '_delete'
    permission_required = {'any': ('inventory_delete_genericproduct',)}


class GenericProductUpdateView(PermissionRequiredMixin, CreateView, UpdateView):
    model = GenericProduct
    template_name_suffix = '_update'
    permission_required = {'any': ('inventory_update_genericproduct',)}
    fields = ['name', 'order', 'status', 'employee', 'stock', 'genericproduct_type', ]
