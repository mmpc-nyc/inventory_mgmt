from inventory.models import Equipment
from inventory.views.base_views import CustomDetailView, CustomListView, CustomCreateView, CustomDeleteView, \
    CustomUpdateView


class EquipmentDetailView(CustomDetailView):
    model = Equipment


class EquipmentListView(CustomListView):
    model = Equipment


class EquipmentCreateView(CustomCreateView):
    model = Equipment


class EquipmentDeleteView(CustomDeleteView):
    model = Equipment


class EquipmentUpdateView(CustomUpdateView):
    model = Equipment
