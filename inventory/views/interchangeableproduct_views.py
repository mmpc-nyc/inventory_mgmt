from inventory.models.product import InterchangeableProduct
from inventory.views.base_views import CustomDetailView, CustomListView, CustomCreateView, CustomDeleteView, \
    CustomUpdateView


class InterchangeableProductDetailView(CustomDetailView):
    model = InterchangeableProduct


class InterchangeableProductListView(CustomListView):
    model = InterchangeableProduct


class InterchangeableProductCreateView(CustomCreateView):
    model = InterchangeableProduct


class InterchangeableProductDeleteView(CustomDeleteView):
    model = InterchangeableProduct


class InterchangeableProductUpdateView(CustomUpdateView):
    model = InterchangeableProduct
