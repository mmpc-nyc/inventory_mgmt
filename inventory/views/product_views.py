from inventory.models.product import Product
from inventory.views.base_views import CustomDetailView, CustomListView, CustomCreateView, CustomDeleteView, \
    CustomUpdateView


class ProductDetailView(CustomDetailView):
    model = Product


class ProductListView(CustomListView):
    model = Product


class ProductCreateView(CustomCreateView):
    model = Product


class ProductDeleteView(CustomDeleteView):
    model = Product


class ProductUpdateView(CustomUpdateView):
    model = Product
