from inventory.models.storage_location import StorageLocation
from inventory.views.base_views import CustomDetailView, CustomListView, CustomCreateView, CustomDeleteView, \
    CustomUpdateView


class StorageLocationDetailView(CustomDetailView):
    model = StorageLocation


class StorageLocationListView(CustomListView):
    model = StorageLocation


class StorageLocationCreateView(CustomCreateView):
    model = StorageLocation


class StorageLocationDeleteView(CustomDeleteView):
    model = StorageLocation


class StorageLocationUpdateView(CustomUpdateView):
    model = StorageLocation

