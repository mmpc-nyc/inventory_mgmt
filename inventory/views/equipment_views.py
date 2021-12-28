from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, DeleteView, UpdateView

from inventory.models import Equipment
from inventory.views.mixins import HTMXDetailView, HTMXListView


class EquipmentDetailView(LoginRequiredMixin, PermissionRequiredMixin, HTMXDetailView):
    model = Equipment
    extra_context = {'title': 'Equipment Detail'}
    permission_required = {'any': ('inventory_view_equipment',)}


class EquipmentListView(LoginRequiredMixin, PermissionRequiredMixin, HTMXListView):
    model = Equipment
    paginate_by = 50
    template_name_suffix = '_list'
    extra_context = {'title': 'Equipment List'}
    permission_required = {'any': ('inventory_view_equipment',)}


class EquipmentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Equipment
    template_name_suffix = '_create'
    permission_required = {'any': ('inventory_create_equipment',)}


class EquipmentDeleteView(PermissionRequiredMixin, CreateView, DeleteView):
    model = Equipment
    template_name_suffix = '_delete'
    permission_required = {'any': ('inventory_delete_equipment',)}


class EquipmentUpdateView(PermissionRequiredMixin, CreateView, UpdateView):
    model = Equipment
    template_name_suffix = '_update'
    permission_required = {'any': ('inventory_update_equipment',)}
    fields = ['name', 'order', 'status', 'employee', 'stock']
