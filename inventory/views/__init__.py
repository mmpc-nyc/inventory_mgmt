from django.shortcuts import render
from django.views.generic import DetailView

from inventory.models import Order


class OrderCheckInView(DetailView):
    model = Order
    template_name_suffix = '_checkin'

class OrderCheckoutView(DetailView):
    model = Order
    template_name_suffix = '_checkout'