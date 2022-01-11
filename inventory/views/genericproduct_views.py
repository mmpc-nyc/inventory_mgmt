from inventory.models import GenericProduct
from inventory.views.base_views import CustomDetailView, CustomListView, CustomCreateView, CustomDeleteView, \
    CustomUpdateView


class GenericProductDetailView(CustomDetailView):
    model = GenericProduct


class GenericProductListView(CustomListView):
    model = GenericProduct


class GenericProductCreateView(CustomCreateView):
    model = GenericProduct


class GenericProductDeleteView(CustomDeleteView):
    model = GenericProduct


class GenericProductUpdateView(CustomUpdateView):
    model = GenericProduct
