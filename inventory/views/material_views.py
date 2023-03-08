from inventory.models.material import Material
from inventory.views.base_views import CustomDetailView, CustomListView, CustomCreateView, CustomDeleteView, \
    CustomUpdateView


class MaterialDetailView(CustomDetailView):
    model = Material


class MaterialListView(CustomListView):
    model = Material


class MaterialCreateView(CustomCreateView):
    model = Material


class MaterialDeleteView(CustomDeleteView):
    model = Material


class MaterialUpdateView(CustomUpdateView):
    model = Material
