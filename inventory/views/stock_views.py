from inventory.models.stock import Stock
from inventory.views.base_views import CustomDetailView, CustomListView, CustomCreateView, CustomDeleteView, \
    CustomUpdateView


class StockDetailView(CustomDetailView):
    model = Stock


class StockListView(CustomListView):
    model = Stock


class StockCreateView(CustomCreateView):
    model = Stock


class StockDeleteView(CustomDeleteView):
    model = Stock


class StockUpdateView(CustomUpdateView):
    model = Stock

