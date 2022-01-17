from dataclasses import dataclass
from typing import Union

from django.db import transaction

from inventory.models.order import Order, Equipment, CollectOrder, DeployOrder, InspectOrder


@dataclass
class OrderFactory:
    model: Union[type(Order)]

    @transaction.atomic
    def create_from_orders(self, date, input_orders, team_lead=None, team=None) -> Order:
        input_orders = [input_orders] if issubclass(type(input_orders), Order) else list(input_orders)
        equipments = set()
        for input_order in input_orders:
            for equipment in input_order.equipments.all():
                equipments.add(equipment)  # TODO Think about broken / decommissioned equipment
        order = self.create_from_equipment(
            date=date,
            customer=input_orders[0].customer,
            location=input_orders[0].location,
            equipments=equipments,
            team_lead=team_lead,
            team=team
        )
        return order

    @transaction.atomic
    def create_from_equipment(self, date, customer, location, equipments, team_lead=None, team=None) -> Order:
        if equipments:
            if isinstance(equipments, Equipment):
                equipments = [equipments]
            else:
                equipments = set(equipments)
        order = self.model.objects.create(
            date=date,
            status=Order.Status.NEW,
            customer=customer,
            location=location,
            team_lead=team_lead,
        )
        for equipment in equipments:
            order.orderequipment_set.create(equipment=equipment, order=order)
        if team:
            for team_member in team:
                order.team.objects.create(team=team_member, order=order)
        order.save()
        return order


collect_order_factory = OrderFactory(model=CollectOrder)
deploy_order_factory = OrderFactory(model=DeployOrder)
inspect_order_factory = OrderFactory(model=InspectOrder)
