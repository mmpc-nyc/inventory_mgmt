from django.utils import timezone

from inventory.models import Order
from test_base import AbstractTest


class TestOrderManager(AbstractTest):
    manager = Order.objects

    def test_create(self):
        order = self.manager.create(customer=self.customer_1, location=self.customer_1_location_1.location,
                                    date=timezone.now())

        if hasattr(self.manager, 'activity'):
            with self.subTest(): self.assertEqual(order.activity, self.manager.activity)

    def test_all(self):
        orders = self.manager.all()
        if hasattr(self.manager, 'activity'):
            with self.subTest():
                for order in orders:
                    self.assertEqual(order.activity, self.manager.activity)


class TestCollectOrderManager(TestOrderManager):
    manager = Order.collect


class TestDeployOrderManager(TestOrderManager):
    manager = Order.deploy


class TestInspectOrderManager(TestOrderManager):
    manager = Order.inspect
