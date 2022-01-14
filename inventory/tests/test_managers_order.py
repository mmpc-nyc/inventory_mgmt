from django.db.models import Manager
from django.utils import timezone

from inventory.models import Order
from test_base import AbstractTest


class ABCContainer:
    class TestAbstractOrderManager(AbstractTest):
        manager: Manager

        def test_create(self):
            self.fail()

        def test_all(self):
            self.fail()


class TestOrderManager(ABCContainer.TestAbstractOrderManager):
    manager = Order.objects

    def test_create(self):
        self.manager.create(customer=self.customer_1, location=self.customer_1_location_1.location, date=timezone.now())

    def test_all(self):
        self.manager.all()


class TestCollectOrderManager(ABCContainer.TestAbstractOrderManager):
    manager = Order.collect

    def test_create_from_one_order(self):
        self.fail()

    def test_create_from_multiple_orders(self):
        self.fail()

    def test_create_using_equipment(self):
        self.fail()


class TestDeployOrderManager(ABCContainer.TestAbstractOrderManager):
    manager = Order.deploy


class TestInspectOrderManager(ABCContainer.TestAbstractOrderManager):
    manager = Order.inspect

    def test_create(self):
        order = self.manager.create(customer=self.customer_1, location=self.customer_1_location_1.location,
                                    date=timezone.now())
        with self.subTest(): self.assertEqual(order.activity, Order.Activity.INSPECT)

    def test_create_from_one_order(self):
        self.fail()

    def test_all(self):
        self.manager.all()
