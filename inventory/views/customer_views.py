from django.views.generic import ListView
from inventory.models.customer import Customer
from inventory.views.base_views import CustomDeleteView, CustomCreateView, CustomDetailView, CustomUpdateView, \
    CustomListView


class CustomerDetailView(CustomDetailView):
    model = Customer


class CustomerListView(CustomListView):
    model = Customer


class CustomerCreateView(CustomCreateView):
    model = Customer


class CustomerDeleteView(CustomDeleteView):
    model = Customer


class CustomerUpdateView(CustomUpdateView):
    model = Customer
