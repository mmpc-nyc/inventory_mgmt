from collections import defaultdict

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import Manager, Max
from django.db.models.query import RawQuerySet
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from inventory.enums import OrderActivity
from inventory.exceptions import OrderCompletionError, ProductConditionError
from inventory.managers.order import OrderManager, DeployOrderManager, InspectOrderManager, CollectOrderManager
from inventory.models.customer import Customer
from inventory.models.location import Location
from inventory.models.product import Product
from inventory.models.warehouse import Warehouse


class Equipment(models.Model):
    """A product that is can be stored, deployed, and picked up. """

    class Status(models.TextChoices):
        """Current status of the product"""

        STORED = 'STORED', _('Stored')  # Equipment stored in Warehouse
        DEPLOYED = 'DEPLOYED', _('Deployed')  # Equipment is currently deployed at order location
        PICKED_UP = 'PICKED_UP', _('Picked Up')  # Equipment is with the employee
        MISSING = 'MISSING', _('Missing')  # Equipment cannot be found.
        DECOMMISSIONED = 'DECOMMISSIONED', _('Decommissioned')

    name = models.CharField(max_length=150, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField(max_length=32, choices=Status.choices, default=Status.STORED)
    warehouse = models.ForeignKey('Warehouse', on_delete=models.SET_NULL, blank=True, null=True)
    condition = models.ForeignKey('Condition', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), related_name='equipment_employee', on_delete=models.SET_NULL, null=True,
                             blank=True)
    location = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Equipment')
        verbose_name_plural = _('Equipment')

    def _check_for_repeat_action(self, order: 'Order', action: 'EquipmentTransactionAction'):
        last_order_transaction_for_this_equipment: 'EquipmentTransaction' = order.equipmenttransaction_set.filter(
            self).last()
        if last_order_transaction_for_this_equipment:
            if last_order_transaction_for_this_equipment.action == action:
                raise ValidationError('Cannot Perform the same action as the last action')

    def _execute(self, action: 'EquipmentTransactionAction', user: get_user_model(), order: 'Order' = None,
                 condition: 'Condition' = None, warehouse: 'Warehouse' = None,
                 recipient: get_user_model() = None) -> 'EquipmentTransaction':
        if not self.condition.has_action(action.name):
            raise ProductConditionError(_(f'This equipment in condition {self.condition} cannot use action {action}'))

        with transaction.atomic():
            self.save()
            warehouse = warehouse or self.warehouse
            condition = condition or self.condition
            return EquipmentTransaction.objects.create(action=action, equipment=self, user=user, condition=condition,
                                                       warehouse=warehouse, order=order, recipient=recipient)

    def decommission(self, user: get_user_model()):
        action = EquipmentTransactionAction.DECOMMISSION
        condition = Condition.objects.get(name='Decommissioned')

        self.user = None
        self.status = self.Status.DECOMMISSIONED
        self.location = None
        self.warehouse = None
        self.condition = condition

        return self._execute(action=action, user=user, condition=condition)

    def collect(self, user: get_user_model(), order: 'Order', condition: 'Condition' = None):
        action = EquipmentTransactionAction.COLLECT

        self.user = user
        self.status = self.Status.PICKED_UP

        return self._execute(action=action, user=user, order=order, condition=condition)

    def deploy(self, user: get_user_model(), order: 'Order', condition: 'Condition' = None):
        action = EquipmentTransactionAction.DEPLOY

        self.status = self.Status.DEPLOYED
        self.location = order.location

        return self._execute(action=action, user=user, order=order, condition=condition)

    def inspect(self, user: get_user_model(), order: 'Order', condition: 'Condition' = None):
        action = EquipmentTransactionAction.INSPECT

        return self._execute(action=action, user=user, order=order, condition=condition)

    def store(self, user: get_user_model(), warehouse: 'Warehouse' = None, condition: 'Condition' = None):
        action = EquipmentTransactionAction.STORE
        warehouse = warehouse or self.warehouse

        self.user = None
        self.location = warehouse.location
        self.status = self.Status.STORED
        self.location = None

        return self._execute(action=action, user=user, condition=condition)

    def transfer(self, recipient: get_user_model(), condition: 'Condition' = None):
        action = EquipmentTransactionAction.TRANSFER
        user = self.user
        self.user = recipient

        return self._execute(action=action, user=user, recipient=recipient, condition=condition)

    def withdraw(self, user: get_user_model(), condition: 'Condition' = None):
        action = EquipmentTransactionAction.WITHDRAW

        self.user = user
        self.status = self.Status.PICKED_UP
        self.location = None

        return self._execute(action=action, user=user, condition=condition)

    def get_absolute_url(self):
        return reverse_lazy('inventory:equipment_detail', kwargs={'pk': self.pk})


class Condition(models.Model):
    """Physical condition of the product that determines if it can be used"""
    name = models.CharField(verbose_name=_('name'), max_length=32)
    description = models.TextField(verbose_name=_('description'))
    action_collect = models.BooleanField(verbose_name=_('collect'), default=False)
    action_decommission = models.BooleanField(verbose_name=_('decommission'), default=False)
    action_deploy = models.BooleanField(verbose_name=_('deploy'), default=False)
    action_store = models.BooleanField(verbose_name=_('store'), default=False)
    action_transfer = models.BooleanField(verbose_name=_('transfer'), default=False)
    action_withdraw = models.BooleanField(verbose_name=_('withdraw'), default=False)

    def __str__(self):
        return f'{self.name}'

    def has_action(self, action_name: str) -> bool:
        formatted_action_name = f'action_{action_name.lower()}'
        if hasattr(self, formatted_action_name):
            return getattr(self, formatted_action_name)
        return False

    class Meta:
        verbose_name = _('Condition')
        verbose_name_plural = _('Conditions')


class EquipmentTransactionAction(models.TextChoices):
    INSPECT = 'Inspect', _('Inspect')
    COLLECT = 'Collect', _('Collect')
    DECOMMISSION = 'Decommission', _('Decommission')
    DEPLOY = 'Deploy', _('Deploy')
    STORE = 'Store', _('Store')
    TRANSFER = 'Transfer', _('Transfer')
    WITHDRAW = 'Withdraw', _('Withdraw')


class EquipmentTransactionManager(Manager):

    def get_order_equipment_transactions_grouped_by_latest_timestamp(self, order: 'Order'):
        return self.filter(order=order).values('equipment').annotate(timestamp=Max('timestamp')).order_by('timestamp')


class EquipmentTransaction(models.Model):
    """A model for managing equipment transactions. Mainly used for logging and auditing"""
    action = models.CharField(max_length=32, choices=EquipmentTransactionAction.choices)
    equipment = models.ForeignKey(Equipment, verbose_name=_('equipment'), on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), verbose_name=_('user'), on_delete=models.CASCADE)
    recipient = models.ForeignKey(get_user_model(), verbose_name=_('recipient'), related_name='recipient',
                                  on_delete=models.CASCADE, blank=True, null=True)
    warehouse = models.ForeignKey('Warehouse', verbose_name=_('warehouse'), on_delete=models.CASCADE, blank=True, null=True)
    condition = models.ForeignKey(Condition, verbose_name=_('condition'), on_delete=models.CASCADE)
    timestamp = models.DateTimeField(verbose_name=_('timestamp'), auto_now=True)
    location = models.ForeignKey('Location', verbose_name=_('Location'), blank=True, null=True,
                                 on_delete=models.CASCADE)
    order = models.ForeignKey('Order', verbose_name=_('Order'), blank=True, null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=32, choices=Equipment.Status.choices)

    objects = EquipmentTransactionManager()

    def clean(self):
        super().clean()

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = _('Equipment Transaction')
        verbose_name_plural = _('Equipment Transactions')


class Order(models.Model):
    """Model for scheduling orders allowing easier assignment of inventory, services and products"""
    COMPLETE_EQUIPMENT_STATUS: str
    ACTIVITY: OrderActivity
    Activity: OrderActivity = OrderActivity

    class Status(models.TextChoices):
        NEW = 'New', _('New')
        ASSIGNED = 'Assigned', _('Assigned')
        IN_PROGRESS = 'In Progress', _('In Progress')
        COMPLETED = 'Completed', _('Completed')
        CANCELED = 'Canceled', _('Canceled')

    parent = models.ManyToManyField('self', related_name='children', symmetrical=False, blank=True, null=True)
    customer = models.ForeignKey(Customer, verbose_name=_('customer'), on_delete=models.CASCADE)
    activity = models.CharField(verbose_name=_('activity'), max_length=32, choices=Activity.choices)
    status = models.CharField(max_length=16, verbose_name=_('status'), choices=Status.choices, default=Status.NEW)
    team_lead = models.ForeignKey(get_user_model(), verbose_name=_('team lead'), related_name='order_team_lead',
                                  on_delete=models.CASCADE, blank=True, null=True)
    team = models.ManyToManyField(get_user_model(), verbose_name=_('team'), related_name='order_team')
    location = models.ForeignKey(Location, verbose_name=_('location'), on_delete=models.CASCADE)
    date = models.DateTimeField()
    equipments = models.ManyToManyField('Equipment', verbose_name=_('equipments'), through='OrderEquipment',
                                        related_name='equipments', null=True)
    generic_products = models.ManyToManyField('GenericProduct', verbose_name=_('generic products'),
                                              through='OrderGenericProduct', related_name='generic_products', null=True)

    objects = OrderManager()

    def validate_order_completion(self):
        if not self.can_complete():
            raise OrderCompletionError('This order cannot be completed.')

    def get_latest_equipment_transactions(self) -> RawQuerySet:
        order_with_transaction = OrderEquipment.objects.raw("""
        select
            inventory_order.id,
            inventory_equipment.id,
            inventory_equipmenttransaction.id as transaction_id,
            inventory_equipmenttransaction.status as transaction_equipment_status,
            inventory_equipmenttransaction.action as transaction_action,
            inventory_equipmenttransaction.user_id as transaction_user_id
        from inventory_order
            left join (
        select o.id as order_id,
               e.id as equipment_id,
               (
                   select et.id as transaction_id
                   from inventory_equipmenttransaction as et
                   where order_id = o.id
                     and equipment_id = e.id
                   order by et.timestamp
                   limit 1
               )    as transaction_id
        from inventory_order as o
                 left join inventory_orderequipment as oe on oe.order_id = o.id
                 left join inventory_equipment as e on oe.equipment_id = e.id
        ) as oet on oet.order_id = inventory_order.id
                 left join inventory_equipment on inventory_equipment.id = oet.equipment_id
                 left join inventory_equipmenttransaction on inventory_equipmenttransaction.id = oet.transaction_id
         where inventory_order.id = %s
        """, [self.id])
        return order_with_transaction

    def can_complete(self) -> bool:
        transactions = self.get_latest_equipment_transactions()
        for transaction_ in transactions:
            if not transaction_.transaction_id:
                return False
        for transaction_ in transactions:
            if transaction_.equipment.status != self.COMPLETE_EQUIPMENT_STATUS:
                return False
        return True

    def perform_equipment_activity(self, equipment: 'Equipment', team_lead: get_user_model() = None):
        ...

    def collect_equipment(self, equipment: 'Equipment', team_lead: get_user_model() = None):
        team_lead = team_lead or self.team_lead
        equipment.collect(user=team_lead, order=self)

    def deploy_equipment(self, equipment: 'Equipment', team_lead: get_user_model() = None):
        team_lead = team_lead or self.team_lead
        equipment.deploy(user=team_lead, order=self)

    def inspect_equipment(self, equipment: 'Equipment', team_lead: get_user_model() = None):
        team_lead = team_lead or self.team_lead
        equipment.deploy(user=team_lead, order=self)

    def complete(self, ignore_issues: bool = False) -> None:
        if not ignore_issues:
            self.validate_order_completion()
        self.status = Order.Status.COMPLETED
        self.save()

    def cancel(self, ignore_issues: bool = False):
        self.status = Order.Status.COMPLETED
        self.save()

    def save(self, **kwargs):
        # TODO Implement a method that only allows updates if the order is in active status.
        return super().save(**kwargs)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return f'{self.id}'


class CollectOrder(Order):
    ACTIVITY = OrderActivity.COLLECT
    COMPLETE_EQUIPMENT_STATUS = Equipment.Status.PICKED_UP
    objects = CollectOrderManager()

    def perform_equipment_activity(self, equipment: 'Equipment', team_lead: get_user_model() = None):
        return self.collect_equipment(team_lead=team_lead, equipment=equipment)

    def complete(self, ignore_issues: bool = False) -> None:
        super().complete(ignore_issues=ignore_issues)

    class Meta:
        verbose_name = _('Collect Order')
        verbose_name_plural = _('Collect Orders')
        proxy = True


class DeployOrder(Order):
    ACTIVITY = OrderActivity.DEPLOY
    COMPLETE_EQUIPMENT_STATUS = Equipment.Status.PICKED_UP
    objects = DeployOrderManager()

    def perform_equipment_activity(self, equipment: 'Equipment', team_lead: get_user_model() = None):
        return self.deploy_equipment(team_lead=team_lead, equipment=equipment)

    def complete(self, ignore_issues: bool = False) -> None:
        if not ignore_issues:
            generic_product_dict = defaultdict(int)
            for order_generic_product in self.ordergenericproduct_set.all():
                generic_product_dict[order_generic_product.generic_product.pk] = order_generic_product.quantity
            for order_equipment in self.orderequipment_set.all():
                related_id = order_equipment.equipment.product.generic_product.id
                if related_id not in generic_product_dict:
                    raise OrderCompletionError(
                        f"""Equipment id {related_id} is not part of requested products {", ".join(map(str, generic_product_dict.keys()))}. enable ignore checks to continue""")
                generic_product_dict[related_id] -= 1
            for generic_product_id, quantity in generic_product_dict.items():
                if quantity != 0:
                    raise OrderCompletionError(
                        'A quantity mismatch was found between requested equipment and deployed equipment. '
                        'To bypass this error ignore checks should be enabled')

        super().complete(ignore_issues=ignore_issues)

    class Meta:
        verbose_name = _('Deploy Order')
        verbose_name_plural = _('Deploy Orders')
        proxy = True


class InspectOrder(Order):
    ACTIVITY = OrderActivity.INSPECT
    objects = InspectOrderManager()

    def perform_equipment_activity(self, equipment: 'Equipment', team_lead: get_user_model() = None):
        return self.inspect_equipment(team_lead=team_lead, equipment=equipment)

    def complete(self, ignore_issues: bool = False) -> None:
        # TODO  Implement this method
        super().complete(ignore_issues=True)

    class Meta:
        verbose_name = _('Inspect Order')
        verbose_name_plural = _('Inspect Orders')
        proxy = True


class OrderGenericProduct(models.Model):
    """A link table for managing the required/recommended generic products needed to fill an order"""

    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    generic_product = models.ForeignKey('GenericProduct', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.order} | {self.generic_product} | {self.quantity}'

    class Meta:
        verbose_name = _('Order Generic Product')
        verbose_name_plural = _('Order Generic Product')
        unique_together = ('order', 'generic_product')


class OrderEquipment(models.Model):
    """A link table for mapping the equipment associated with the order"""
    # TODO Create order transactions that keep track of when equipment was picked up.

    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    equipment = models.ForeignKey('Equipment', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.order} | {self.equipment}'

    class Meta:
        verbose_name = _('Order Equipment')
        verbose_name_plural = _('Order Equipment')
        unique_together = ('order', 'equipment')
