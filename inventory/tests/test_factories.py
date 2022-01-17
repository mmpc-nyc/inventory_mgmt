from django.utils import timezone

from inventory.factories import collect_order_factory, deploy_order_factory, inspect_order_factory
from inventory.models.order import Order, Equipment
from inventory.tests import AbstractTest


class TestCollectOrderFactory(AbstractTest):
    factories = [collect_order_factory, deploy_order_factory, inspect_order_factory]

    def test_create_from_orders(self):
        # TODO Add validation and integrity checks
        for factory in self.factories:
            with self.subTest(factory):
                input_order = self.order_deploy_complete
                order_collections = [input_order, [input_order, ], (input_order,), {input_order, }, Order.objects.all()]
                for input_orders in order_collections:
                    input_orders = [input_orders] if issubclass(type(input_orders), Order) else input_orders
                    output_order = factory.create_from_orders(date=timezone.now(), input_orders=input_orders)
                    self.assertEqual(output_order.activity, factory.model.ACTIVITY)
                    self.assertTrue(isinstance(output_order, Order))
                    input_equipment_set = set()
                    for input_order in input_orders:
                        for equipment in input_order.equipments.all():
                            input_equipment_set.add(equipment)
                    output_equipment_set = set()
                    for order_equipment in output_order.orderequipment_set.all():
                        output_equipment_set.add(order_equipment.equipment)
                    self.assertEqual(input_equipment_set, output_equipment_set)

    def test_create_from_equipment(self):
        # TODO Add validation and integrity checks
        for factory in self.factories:
            with self.subTest(factory):
                input_equipment = self.equipment_deployed_working_1
                equipment_collections = [input_equipment, [input_equipment, ], (input_equipment,), {input_equipment, },
                                         Equipment.objects.all()]
                for input_equipments in equipment_collections:
                    input_equipments = [input_equipments] if issubclass(type(input_equipments),
                                                                        Equipment) else input_equipments
                    output_order = factory.create_from_equipment(
                        date=timezone.now(),
                        customer=self.order_deploy_complete.customer,
                        location=self.order_deploy_complete.location,
                        equipments=input_equipments
                    )
                    self.assertEqual(output_order.activity, factory.model.ACTIVITY)
                    self.assertTrue(isinstance(output_order, Order))
                    input_equipment_set = set()
                    for equipment in input_equipments:
                        input_equipment_set.add(equipment)
                    output_equipment_set = set()
                    for order_equipment in output_order.orderequipment_set.all():
                        output_equipment_set.add(order_equipment.equipment)
                    self.assertEqual(input_equipment_set, output_equipment_set)
