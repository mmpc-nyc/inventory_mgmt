from typing import Union

from django.db import transaction
from django.db.models import QuerySet

from inventory.enums import OrderActivity
from inventory.models.order import Order, Equipment


class OrderFactory:
    activity: OrderActivity

    def create_from_orders(self, date, orders: Union[Order, list[Order], tuple[Order], QuerySet]) -> Order:
        if isinstance(orders, Order):
            orders = [orders]
        equipments = set()
        for order in orders:
            for equipment in order.equipments.all():
                equipments.add(equipment)  # TODO Think about broken / decommissioned equipment
        with transaction.atomic():
            order = Order(activity=self.activity, date=date, status=Order.Status.NEW, customer=orders[0].customer,
                          location=orders[0].location)
            for equipment in equipments:
                order.equipmenttransaction_set.add(equipment)
            order.save()
            return order

    def create_from_equipment(self, date, customer, location, equipments: Union[
        Equipment, list[Equipment], tuple[Equipment], set[Equipment], QuerySet] = None) -> Order:
        if equipments:
            if isinstance(equipments, Equipment):
                equipments = [equipments]
        with transaction.atomic():
            order = Order(activity=self.activity, date=date, status=Order.Status.NEW, customer=customer,
                          location=location)
            for equipment in equipments:
                order.equipmenttransaction_set.add(equipment)
            order.save()
            return order