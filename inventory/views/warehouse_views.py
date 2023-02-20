from inventory.models.stock_location import StockLocation
from inventory.views.base_views import CustomDetailView, CustomListView, CustomCreateView, CustomDeleteView, \
    CustomUpdateView


class StockLocationDetailView(CustomDetailView):
    model = StockLocation


class StockLocationListView(CustomListView):
    model = StockLocation


class StockLocationCreateView(CustomCreateView):
    model = StockLocation


class StockLocationDeleteView(CustomDeleteView):
    model = StockLocation


class StockLocationUpdateView(CustomUpdateView):
    model = StockLocation

