from django.contrib.auth import get_user_model
from django.test import TestCase

from inventory.models import Equipment, Stock, Condition, Location, EquipmentTransaction, EquipmentAction, Order

User = get_user_model()


class TestEquipmentTransactionManager(TestCase):

    fixtures = ['fixtures/db.json',]

    def setUp(self):
        self.equipment = Equipment.objects.get(id=1)
        self.user = User.objects.get(username='test_user1')
        self.recipient = User.objects.get(username='test_user2')
        self.stock = Stock.objects.get(id=1)
        self.condition = Condition.objects.get(id=1)
        self.location = Location.objects.get(id=1)
        self.order = Order.objects.get(id=1)

    def test_collect(self):
        transaction = EquipmentTransaction.actions.collect(
            user=self.user,
            equipment=self.equipment,
            condition=None,
        )
        with self.subTest(): self.assertEqual(transaction.action, EquipmentAction.COLLECT)
        with self.subTest(): self.assertEqual(transaction.equipment.status, self.equipment.Status.PICKED_UP)

        with self.subTest(): self.assertEqual(transaction.user, self.user)
        with self.subTest(): self.assertIsNone(transaction.recipient)
        with self.subTest(): self.assertEqual(transaction.condition, transaction.equipment.condition)
        with self.subTest(): self.assertEqual(transaction.stock, transaction.equipment.stock)

    def test_decommission(self):
        transaction = EquipmentTransaction.actions.decommission(
            user=self.user,
            equipment=self.equipment,
        )
        with self.subTest(): self.assertEqual(transaction.action, EquipmentAction.DECOMMISSION)
        with self.subTest(): self.assertEqual(transaction.equipment.status, self.equipment.Status.DECOMMISSIONED)

        with self.subTest(): self.assertIsNone(transaction.recipient)
        with self.subTest(): self.assertIsNone(transaction.stock)
        with self.subTest(): self.assertIsNone(transaction.equipment.user)

        with self.subTest(): self.assertIsNone(transaction.equipment.location)
        with self.subTest(): self.assertEqual(transaction.condition, transaction.equipment.condition)

    def test_deploy(self):
        transaction = EquipmentTransaction.actions.deploy(
            user=self.user,
            equipment=self.equipment,
            location= self.location,
            condition=None,
        )
        with self.subTest(): self.assertEqual(transaction.action, EquipmentAction.DEPLOY)
        with self.subTest(): self.assertEqual(transaction.equipment.status, self.equipment.Status.DEPLOYED)
        with self.subTest(): self.assertEqual(transaction.user, self.user)
        with self.subTest(): self.assertIsNone(transaction.recipient)
        with self.subTest(): self.assertEqual(transaction.condition, transaction.equipment.condition)
        with self.subTest(): self.assertEqual(transaction.stock, transaction.equipment.stock)

    def test_store(self):
        transaction = EquipmentTransaction.actions.store(
            user=self.user,
            equipment=self.equipment,
            stock=self.stock,
            condition=None,
        )
        with self.subTest(): self.assertEqual(transaction.action, EquipmentAction.STORE)
        with self.subTest(): self.assertEqual(transaction.equipment.status, self.equipment.Status.STORED)
        with self.subTest(): self.assertIsNone(transaction.equipment.user)
        with self.subTest(): self.assertEqual(transaction.user, self.user)
        with self.subTest(): self.assertIsNone(transaction.recipient)
        with self.subTest(): self.assertEqual(transaction.condition, transaction.equipment.condition)
        with self.subTest(): self.assertEqual(transaction.stock, transaction.equipment.stock)
        with self.subTest(): self.assertEqual(transaction.stock, self.stock)

    def test_transfer(self):
        transaction = EquipmentTransaction.actions.transfer(
            recipient=self.recipient,
            equipment=self.equipment,
            condition=None,
        )
        with self.subTest(): self.assertEqual(transaction.action, EquipmentAction.TRANSFER)
        with self.subTest(): self.assertEqual(transaction.equipment.status, self.equipment.Status.PICKED_UP)
        with self.subTest(): self.assertEqual(transaction.user, self.user)
        with self.subTest(): self.assertEqual(self.recipient, transaction.recipient)
        with self.subTest(): self.assertNotEqual(transaction.equipment.user, self.user)
        with self.subTest(): self.assertEqual(transaction.equipment.user, self.recipient)
        with self.subTest(): self.assertIsNone(transaction.recipient)
        with self.subTest(): self.assertEqual(transaction.condition, transaction.equipment.condition)
        with self.subTest(): self.assertEqual(transaction.stock, transaction.equipment.stock)

    def test_withdraw(self):
        transaction = EquipmentTransaction.actions.withdraw(
            user=self.user,
            equipment=self.equipment,
            condition=None,
        )
        with self.subTest(): self.assertEqual(transaction.action, EquipmentAction.WITHDRAW)
        with self.subTest(): self.assertEqual(transaction.equipment.status, self.equipment.Status.PICKED_UP)
        with self.subTest(): self.assertEqual(transaction.user, self.user)
        with self.subTest(): self.assertIsNone(transaction.recipient)
        with self.subTest(): self.assertEqual(transaction.condition, transaction.equipment.condition)
        with self.subTest(): self.assertEqual(transaction.stock, transaction.equipment.stock)