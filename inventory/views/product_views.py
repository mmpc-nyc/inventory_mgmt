from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView
from inventory.models import Product


class ProductDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Product
    template_name_suffix = '_detail'
    extra_context = {'title': 'Product Detail'}
    permission_required = {'any': ('inventory_view_product',)}


class ProductListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Product
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
