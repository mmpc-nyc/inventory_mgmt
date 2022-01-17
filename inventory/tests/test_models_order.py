from inventory.exceptions import OrderCompletionError
from inventory.models.order import Order
from inventory.tests import AbstractTest


class TestOrder(AbstractTest):

    def test_complete_collect_initial(self):
        order = self.order_collect_initial
        with self.subTest():
            with self.assertRaises(OrderCompletionError):
                order.complete()
        order.complete(ignore_issues=True)
        with self.subTest(): self.assertEqual(order.activity, Order.Activity.COLLECT)
        with self.subTest(): self.assertEqual(order.status, Order.Status.COMPLETED)

    def test_complete_collect_partial(self):
        order = self.order_collect_partial
        with self.subTest():
            with self.assertRaises(OrderCompletionError):
                order.complete()
        order.complete(ignore_issues=True)
        with self.subTest(): self.assertEqual(order.activity, Order.Activity.COLLECT)
        with self.subTest(): self.assertEqual(order.status, Order.Status.COMPLETED)

    def test_complete_collect_complete(self):
        order = self.order_collect_complete
        order.complete()
        with self.subTest(): self.assertEqual(order.activity, Order.Activity.COLLECT)
        with self.subTest(): self.assertEqual(order.status, Order.Status.COMPLETED)

    def test_complete_deploy_initial(self):
        order = self.order_deploy_initial
        with self.subTest():
            with self.assertRaises(OrderCompletionError):
                order.complete()
        order.complete(ignore_issues=True)
        with self.subTest(): self.assertEqual(order.activity, Order.Activity.DEPLOY)
        with self.subTest(): self.assertEqual(order.status, Order.Status.COMPLETED)

    def test_complete_deploy_partial(self):
        order = self.order_deploy_partial
        with self.subTest():
            with self.assertRaises(OrderCompletionError):
                order.complete()
        order.complete(ignore_issues=True)
        with self.subTest(): self.assertEqual(order.activity, Order.Activity.DEPLOY)
        with self.subTest(): self.assertEqual(order.status, Order.Status.COMPLETED)

    def test_complete_deploy_complete(self):
        order = self.order_deploy_complete
        order.complete()
        with self.subTest(): self.assertEqual(order.activity, Order.Activity.DEPLOY)
        with self.subTest(): self.assertEqual(order.status, Order.Status.COMPLETED)

    def test_complete_inspect(self):
        order = self.order_inspect
        order.complete()
        with self.subTest(): self.assertEqual(order.activity, Order.Activity.INSPECT)
        with self.subTest(): self.assertEqual(order.status, Order.Status.COMPLETED)
