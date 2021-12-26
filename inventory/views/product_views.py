from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, DeleteView, UpdateView

from inventory.filters import ProductFilter
from inventory.models import Product
from inventory.views.mixins import HTMXDetailView, HTMXListView


class ProductDetailView(LoginRequiredMixin, PermissionRequiredMixin, HTMXDetailView):
    model = Product
    extra_context = {'title': 'Product Detail'}
    permission_required = {'any': ('inventory_view_product',)}


class ProductListView(LoginRequiredMixin, PermissionRequiredMixin, HTMXListView):
    model = Product
    filterset_class = ProductFilter
    paginate_by = 50
    template_name_suffix = '_list'
    extra_context = {'title': 'Product List'}
    permission_required = {'any': ('inventory_view_product',)}


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    template_name_suffix = '_create'
    permission_required = {'any': ('inventory_create_product',)}


class ProductDeleteView(PermissionRequiredMixin, CreateView, DeleteView):
    model = Product
    template_name_suffix = '_delete'
    permission_required = {'any': ('inventory_delete_product',)}


class ProductUpdateView(PermissionRequiredMixin, CreateView, UpdateView):
    model = Product
    template_name_suffix = '_update'
    permission_required = {'any': ('inventory_update_product',)}
    fields = ['name', 'job', 'status', 'employee', 'stock', 'product_type', ]
