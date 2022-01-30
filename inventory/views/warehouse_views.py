from inventory.models.warehouse import Warehouse
from inventory.views.base_views import CustomDetailView, CustomListView, CustomCreateView, CustomDeleteView, \
    CustomUpdateView


class WarehouseDetailView(CustomDetailView):
    model = Warehouse


class WarehouseListView(CustomListView):
    model = Warehouse


class WarehouseCreateView(CustomCreateView):
    model = Warehouse


class WarehouseDeleteView(CustomDeleteView):
    model = Warehouse


class WarehouseUpdateView(CustomUpdateView):
    model = Warehouse

