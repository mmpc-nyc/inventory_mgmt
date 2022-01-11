from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from inventory.exceptions import TransactionError, ProductConditionError, UserAuthorizationError
from inventory.models import EquipmentTransaction, EquipmentTransactionAction, Location, Equipment, Condition, Stock

User = get_user_model()


class Action:
    name: str
    description: str
    equipment_transaction_action: EquipmentTransactionAction
    equipment: Equipment
    user: User
    stock: Stock = None
    condition: Condition = None
    recipient: User = None
    location: Location = None
    equipment_transaction: EquipmentTransaction = None

    def __init__(self, equipment: Equipment, user: User, condition: condition = None, stock: Stock = None,
                 recipient: User = None):
        self.equipment = equipment
        self.equipment.condition = condition or equipment.condition
        self.condition = self.equipment.condition
        self.stock = stock
        self.user = user or equipment.user
        self.recipient = recipient
        self.validate()

    def is_authorized(self):
        # TODO Implement user authorization
        return True

    def validate(self):
        if len(self.name) > 32:
            raise ValueError(f'The transaction action name cannot be longer than 32 characters.')
        if not self.is_authorized():
            raise UserAuthorizationError(
                _(f'User {self.user} is not authorized to perform action {self.equipment_transaction_action}'))
        if not self.condition.actions.filter(id=self.get_equipment_transaction_action().id).exists():
            raise ProductConditionError(_(
                f'This equipment in condition {self.condition} cannot use action {self.equipment_transaction_action}'))

    def get_equipment_transaction(self) -> EquipmentTransaction:
        equipment_transaction = EquipmentTransaction(equipment=self.equipment,
                                                     action=self.get_equipment_transaction_action(), user=self.user,
                                                     condition=self.condition, stock=self.stock,
                                                     recipient=self.recipient, )
        return equipment_transaction

    def get_equipment_transaction_action(self) -> EquipmentTransactionAction:
        self.equipment_transaction_action = EquipmentTransactionAction.objects.get(name=self.name)
        print(self.equipment_transaction_action)
        return self.equipment_transaction_action

    def execute(self):
        with transaction.atomic():
            self.equipment_transaction = self.get_equipment_transaction()
            self.equipment.save()
            self.equipment_transaction.save()
        return self.equipment_transaction


class StoreAction(Action):
    name = 'Store'
    description = 'Stores equipment at stock location'

    def validate(self):
        if not self.stock:
            raise TypeError('Stock must be supplied when storing equipment')
        super().validate()

    def execute(self):
        self.equipment.stock = self.stock or self.equipment.stock
        self.equipment.user = None
        self.equipment.status = self.equipment.Status.STORED
        self.equipment.location = self.stock.location
        self.location = self.stock.location

        return super().execute()


class PickUpAction(Action):
    name = 'Pick Up'
    description = 'Pick Up equipment from customer location'

    def execute(self) -> EquipmentTransaction:
        self.equipment.stock = self.stock or self.equipment.stock
        self.equipment.user = self.user
        self.equipment.status = self.equipment.Status.PICKED_UP
        self.equipment.location = self.stock.location

        return super().execute()


class DeployAction(Action):
    name = 'Deploy'
    description = 'Deploy equipment at customer location'

    location: Location

    def execute(self) -> EquipmentTransaction:
        self.equipment.status = self.equipment.Status.DEPLOYED
        self.equipment.location = self.location

        return super().execute()


class TransferAction(Action):
    name = 'Transfer'
    description = 'Transfer equipment from one user to another'

    def validate(self):
        if not self.recipient:
            raise TypeError('Transfer action requires a recipient to be defined')
        if self.user == self.recipient:
            raise TransactionError("Cannot transfer item to yourself")
        return super().validate()

    def execute(self) -> EquipmentTransaction:

        self.equipment.user = self.recipient
        self.equipment.status = self.equipment.Status.PICKED_UP
        self.equipment.location = self.recipient.location
        return super().execute()


class Decommission(Action):
    name = 'Decommission'
    description = 'Decommission equipment. It cannot be used or repaired'

    def execute(self) -> EquipmentTransaction:
        self.equipment.user = None
        self.equipment.stock = None
        self.equipment.status = self.equipment.Status.DECOMMISSIONED
        return super().execute()


class Withdraw(Action):
    name = 'Withdraw'
    description = 'Withdraw equipment from stock location'

    def execute(self):
        self.equipment.user = self.user
        self.equipment.status = self.equipment.Status.PICKED_UP
        return super().execute()
