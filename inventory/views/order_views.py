from inventory.models import Order
from inventory.views.base_views import CustomDetailView, CustomListView, CustomCreateView, CustomDeleteView, \
    CustomUpdateView


class OrderDetailView(CustomDetailView):
    model = Order


class OrderListView(CustomListView):
    model = Order


class OrderCreateView(CustomCreateView):
    model = Order


class OrderDeleteView(CustomDeleteView):
    model = Order


class OrderUpdateView(CustomUpdateView):
    model = Order