from django.utils import timezone

from inventory.models.order import Order, CollectOrder, DeployOrder, InspectOrder
from inventory.tests import AbstractTest


class TestOrderManager(AbstractTest):
    manager = Order.objects

    def test_create(self):
        manager = self.manager.create(customer=self.customer_1, location=self.customer_1_location_1.location,
                                      date=timezone.now())

        if hasattr(self.manager, 'activity'):
            with self.subTest(): self.assertEqual(manager.activity, self.manager.activity)

    def test_all(self):
        orders = self.manager.all()
        if hasattr(self.manager, 'activity'):
            with self.subTest():
                for order in orders:
                    self.assertEqual(order.activity, self.manager.activity)


class TestCollectOrderManager(TestOrderManager):
    manager = CollectOrder.objects


class TestDeployOrderManager(TestOrderManager):
    manager = DeployOrder.objects


class TestInspectOrderManager(TestOrderManager):
    manager = InspectOrder.objects
