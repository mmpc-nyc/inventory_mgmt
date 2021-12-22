from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import inlineformset_factory
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView
from inventory.models import Stock, Location


class StockDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Stock
    template_name_suffix = '_detail'
    extra_context = {'title': 'Inventory Detail'}
    permission_required = {'any': 'inventory_view_inventory'}


class StockListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Stock
    template_name_suffix = '_list'
    extra_context = {'title': 'Inventory List'}
    permission_required = {'any': 'inventory_view_inventory'}


class StockCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    #  TODO  Fix this broken formset
    form_class = inlineformset_factory(
        Location,
        Stock,
        fk_name='location',
        fields=('name', 'status', 'location', 'location__raw')
    )
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

