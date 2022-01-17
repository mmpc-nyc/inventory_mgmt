from inventory.models.order import EquipmentTransactionAction
from inventory.tests import AbstractTest


class TestEquipmentTransactionManager(AbstractTest):

    def test_collect(self):
        transaction = self.equipment_stored_working.collect(user=self.user, order=self.order_collect_complete,
                                                            condition=None)
        with self.subTest(): self.assertEqual(transaction.action, EquipmentTransactionAction.COLLECT)
        with self.subTest(): self.assertEqual(transaction.equipment.status,
                                              self.equipment_stored_working.Status.PICKED_UP)

        with self.subTest(): self.assertEqual(transaction.user, self.user)
        with self.subTest(): self.assertIsNone(transaction.recipient)
        with self.subTest(): self.assertEqual(transaction.condition, transaction.equipment.condition)
        with self.subTest(): self.assertEqual(transaction.stock, transaction.equipment.stock)

    def test_decommission(self):
        transaction = self.equipment_picked_up_working_1.decommission(user=self.user, )
        with self.subTest(): self.assertEqual(transaction.action, EquipmentTransactionAction.DECOMMISSION)
        with self.subTest(): self.assertEqual(transaction.equipment.status,
                                              self.equipment_stored_working.Status.DECOMMISSIONED)

        with self.subTest(): self.assertIsNone(transaction.recipient)
        with self.subTest(): self.assertIsNone(transaction.stock)
        with self.subTest(): self.assertIsNone(transaction.equipment.user)

        with self.subTest(): self.assertIsNone(transaction.equipment.location)
        with self.subTest(): self.assertEqual(transaction.condition, transaction.equipment.condition)

    def test_deploy(self):
        transaction = self.equipment_picked_up_working_1.deploy(user=self.user, order=self.order_deploy_complete,
                                                                condition=None)
        with self.subTest(): self.assertEqual(transaction.action, EquipmentTransactionAction.DEPLOY)
        with self.subTest(): self.assertEqual(transaction.equipment.status,
                                              self.equipment_stored_working.Status.DEPLOYED)
        with self.subTest(): self.assertEqual(transaction.user, self.user)
        with self.subTest(): self.assertIsNone(transaction.recipient)
        with self.subTest(): self.assertEqual(transaction.condition, transaction.equipment.condition)
        with self.subTest(): self.assertEqual(transaction.stock, transaction.equipment.stock)

    def test_store(self):
        transaction = self.equipment_picked_up_working_1.store(user=self.user, stock=self.stock, condition=None, )
        with self.subTest(): self.assertEqual(transaction.action, EquipmentTransactionAction.STORE)
        with self.subTest(): self.assertEqual(transaction.equipment.status, self.equipment_stored_working.Status.STORED)
        with self.subTest(): self.assertIsNone(transaction.equipment.user)
        with self.subTest(): self.assertEqual(transaction.user, self.user)
        with self.subTest(): self.assertIsNone(transaction.recipient)
        with self.subTest(): self.assertEqual(transaction.condition, transaction.equipment.condition)
        with self.subTest(): self.assertEqual(transaction.stock, transaction.equipment.stock)
        with self.subTest(): self.assertEqual(transaction.stock, self.stock)

    def test_transfer(self):
        transaction = self.equipment_picked_up_working_1.transfer(recipient=self.recipient, condition=None, )
        with self.subTest(): self.assertEqual(transaction.action, EquipmentTransactionAction.TRANSFER)
        with self.subTest(): self.assertEqual(transaction.equipment.status,
                                              self.equipment_stored_working.Status.PICKED_UP)
        with self.subTest(): self.assertEqual(transaction.user, self.user)
        with self.subTest(): self.assertEqual(transaction.recipient, self.recipient)
        with self.subTest(): self.assertNotEqual(transaction.equipment.user, self.user)
        with self.subTest(): self.assertEqual(transaction.equipment.user, self.recipient)
        with self.subTest(): self.assertEqual(transaction.condition, transaction.equipment.condition)
        with self.subTest(): self.assertEqual(transaction.stock, transaction.equipment.stock)

    def test_withdraw(self):
        transaction = self.equipment_stored_working.withdraw(user=self.user, condition=None, )
        with self.subTest(): self.assertEqual(transaction.action, EquipmentTransactionAction.WITHDRAW)
        with self.subTest(): self.assertEqual(transaction.equipment.status,
                                              self.equipment_stored_working.Status.PICKED_UP)
        with self.subTest(): self.assertEqual(transaction.user, self.user)
        with self.subTest(): self.assertIsNone(transaction.recipient)
        with self.subTest(): self.assertEqual(transaction.condition, transaction.equipment.condition)
        with self.subTest(): self.assertEqual(transaction.stock, transaction.equipment.stock)
