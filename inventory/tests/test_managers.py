from inventory.models import EquipmentTransaction, EquipmentTransactionAction
from test_base import AbstractTest


class TestEquipmentTransactionManager(AbstractTest):

    def test_collect(self):
        transaction = EquipmentTransaction.objects.collect(user=self.user, equipment=self.equipment_stored_working,
                                                           condition=None, )
        with self.subTest(): self.assertEqual(transaction.action, EquipmentTransactionAction.COLLECT)
        with self.subTest(): self.assertEqual(transaction.equipment.status,
                                              self.equipment_stored_working.Status.PICKED_UP)

        with self.subTest(): self.assertEqual(transaction.user, self.user)
        with self.subTest(): self.assertIsNone(transaction.recipient)
        with self.subTest(): self.assertEqual(transaction.condition, transaction.equipment.condition)
        with self.subTest(): self.assertEqual(transaction.stock, transaction.equipment.stock)

    def test_decommission(self):
        transaction = EquipmentTransaction.objects.decommission(user=self.user,
                                                                equipment=self.equipment_picked_up_working, )
        with self.subTest(): self.assertEqual(transaction.action, EquipmentTransactionAction.DECOMMISSION)
        with self.subTest(): self.assertEqual(transaction.equipment.status,
                                              self.equipment_stored_working.Status.DECOMMISSIONED)

        with self.subTest(): self.assertIsNone(transaction.recipient)
        with self.subTest(): self.assertIsNone(transaction.stock)
        with self.subTest(): self.assertIsNone(transaction.equipment.user)

        with self.subTest(): self.assertIsNone(transaction.equipment.location)
        with self.subTest(): self.assertEqual(transaction.condition, transaction.equipment.condition)

    def test_deploy(self):
        transaction = EquipmentTransaction.objects.deploy(user=self.user, equipment=self.equipment_picked_up_working,
                                                          location=self.location_customer, condition=None, )
        with self.subTest(): self.assertEqual(transaction.action, EquipmentTransactionAction.DEPLOY)
        with self.subTest(): self.assertEqual(transaction.equipment.status,
                                              self.equipment_stored_working.Status.DEPLOYED)
        with self.subTest(): self.assertEqual(transaction.user, self.user)
        with self.subTest(): self.assertIsNone(transaction.recipient)
        with self.subTest(): self.assertEqual(transaction.condition, transaction.equipment.condition)
        with self.subTest(): self.assertEqual(transaction.stock, transaction.equipment.stock)

    def test_store(self):
        transaction = EquipmentTransaction.objects.store(user=self.user, equipment=self.equipment_picked_up_working,
                                                         stock=self.stock, condition=None, )
        with self.subTest(): self.assertEqual(transaction.action, EquipmentTransactionAction.STORE)
        with self.subTest(): self.assertEqual(transaction.equipment.status, self.equipment_stored_working.Status.STORED)
        with self.subTest(): self.assertIsNone(transaction.equipment.user)
        with self.subTest(): self.assertEqual(transaction.user, self.user)
        with self.subTest(): self.assertIsNone(transaction.recipient)
        with self.subTest(): self.assertEqual(transaction.condition, transaction.equipment.condition)
        with self.subTest(): self.assertEqual(transaction.stock, transaction.equipment.stock)
        with self.subTest(): self.assertEqual(transaction.stock, self.stock)

    def test_transfer(self):
        transaction = EquipmentTransaction.objects.transfer(recipient=self.recipient,
                                                            equipment=self.equipment_picked_up_working,
                                                            condition=None, )
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
        transaction = EquipmentTransaction.objects.withdraw(user=self.user, equipment=self.equipment_stored_working,
                                                            condition=None, )
        with self.subTest(): self.assertEqual(transaction.action, EquipmentTransactionAction.WITHDRAW)
        with self.subTest(): self.assertEqual(transaction.equipment.status,
                                              self.equipment_stored_working.Status.PICKED_UP)
        with self.subTest(): self.assertEqual(transaction.user, self.user)
        with self.subTest(): self.assertIsNone(transaction.recipient)
        with self.subTest(): self.assertEqual(transaction.condition, transaction.equipment.condition)
        with self.subTest(): self.assertEqual(transaction.stock, transaction.equipment.stock)


class TestCollectOrderManager(AbstractTest):
    pass


class TestDeployOrderManager(AbstractTest):
    pass


class TestInspectOrderManager(AbstractTest):
    pass
