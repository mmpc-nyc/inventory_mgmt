from collections import defaultdict

from django.contrib.auth import get_user_model
from django.db import models, transaction
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from inventory.exceptions import OrderCompletionError, ProductConditionError, StockLogicError, ProductStatusError, \
    TransactionError
from inventory.models.customer import Customer
from inventory.models.location import Location


class Order(models.Model):
    """Model for scheduling orders to allow easier assignment of inventory, services and products"""

    class Activity(models.TextChoices):
        DEPLOY = 'Deploy', _('Deploy')
        PICKUP = 'Pickup', _('Pickup')
        INSPECT = 'Inspect', _('Inspect')

    class Status(models.TextChoices):
        NEW = 'New', _('New')
        ASSIGNED = 'Assigned', _('Assigned')
        IN_PROGRESS = 'In Progress', _('In Progress')
        COMPLETED = 'Completed', _('Completed')
        CANCELED = 'Canceled', _('Canceled')

    customer = models.ForeignKey(Customer, verbose_name=_('customer'), on_delete=models.CASCADE)
    activity = models.CharField(verbose_name=_('activity'), max_length=32, choices=Activity.choices,
                                default=Activity.DEPLOY)
    status = models.CharField(max_length=16, verbose_name=_('status'), choices=Status.choices, default=Status.NEW)
    employees = models.ManyToManyField(get_user_model(), verbose_name=_('employees'), related_name='order_employees')
    location = models.ForeignKey(Location, verbose_name=_('location'), on_delete=models.CASCADE)
    date = models.DateTimeField()
    equipments = models.ManyToManyField('Equipment', verbose_name=_('equipments'), through='OrderEquipment',
                                        related_name='equipments')
    generic_products = models.ManyToManyField('GenericProduct', verbose_name=_('generic products'),
                                              through='OrderGenericProduct', related_name='generic_products')
    history = HistoricalRecords()

    def get_deployed_equipment(self):
        return self.equipments.filter(status=Equipment.Status.DEPLOYED)

    def missing_equipment_validator(self, ignore_issues: True):
        """If there is any equipment that is still deployed the completion will fail unless the
        "ignore_issues" is true then the status of the remaining deployed equipment will
        be set to MISSING"""

        deployed_equipment = self.get_deployed_equipment()
        if deployed_equipment:
            if not ignore_issues:
                raise OrderCompletionError('Not all equipment has been picked up')
            deployed_equipment.update(status=Equipment.Status.MISSING)

    def complete(self, ignore_issues: bool = False):
        """Completes the order"""
        if self.status in {self.Status.COMPLETED, self.Status.CANCELED}:
            raise OrderCompletionError(f'Cannot complete order with status of {self.status}')
        if self.activity == self.Activity.DEPLOY:
            self._complete_deploy_activity(ignore_issues=ignore_issues)
        elif self.activity == self.Activity.PICKUP:
            self._complete_pickup_activity(ignore_issues=ignore_issues)
        elif self.activity == self.Activity.INSPECT:
            self._complete_inspection_activity(ignore_issues=ignore_issues)
        self.status = self.Status.COMPLETED
        self.save()

    def _complete_deploy_activity(self, ignore_issues: bool):
        if self.activity != self.Activity.DEPLOY:
            return
        if ignore_issues:
            return

        generic_product_dict = defaultdict(int)
        for order_generic_product in self.ordergenericproduct_set.all():
            generic_product_dict[order_generic_product.pk] = order_generic_product.quantity
        for order_equipment in self.orderequipment_set.all():
            related_id = order_equipment.equipment.product.generic_product.id
            if related_id not in generic_product_dict:
                raise OrderCompletionError(
                    'Equipment that is not part of the order cannot be deployed unless ignore checks is enabled')
            generic_product_dict[related_id] -= 1
        for generic_product_id, quantity in generic_product_dict.items():
            if quantity != 0:
                raise OrderCompletionError(
                    'A quantity mismatch was found between requested equipment and deployed equipment. '
                    'To bypass this error ignore checks should be enabled')

    def _complete_pickup_activity(self, ignore_issues: bool):
        self.missing_equipment_validator(ignore_issues)

    def _complete_inspection_activity(self, ignore_issues: bool):
        ...

    def cancel(self, ignore_issues: bool = False):
        """Cancels the order"""
        self.missing_equipment_validator(ignore_issues=ignore_issues)
        self.status = self.Status.CANCELED
        self.save()

    def save(self, **kwargs):
        # TODO Implement a method that only allows updates if the order is in active status.
        if self.status:
            ...
        return super().save(**kwargs)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return f'{self.id}'


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

    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    equipment = models.ForeignKey('Equipment', on_delete=models.CASCADE)
    deployed = models.DateTimeField()
    picked_up = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.order} | {self.equipment}'

    class Meta:
        verbose_name = _('Order Equipment')
        verbose_name_plural = _('Order Equipment')
        unique_together = ('order', 'equipment')


User = get_user_model()


class Equipment(models.Model):
    """A product that is can be stored, deployed, and picked up. """

    class Status(models.TextChoices):
        """Current status of the product"""

        STORED = 'STORED', _('Stored')  # Equipment stored in Stock
        DEPLOYED = 'DEPLOYED', _('Deployed')  # Equipment is currently deployed at order location
        PICKED_UP = 'PICKED_UP', _('Picked Up')  # Equipment is with the employee
        MISSING = 'MISSING', _('Missing')  # Equipment cannot be found.

    name = models.CharField(max_length=150, blank=True, null=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    status = models.CharField(max_length=32, choices=Status.choices, default=Status.STORED)
    stock = models.ForeignKey('Stock', on_delete=models.SET_NULL, blank=True, null=True)
    condition = models.ForeignKey('Condition', on_delete=models.PROTECT)
    employee = models.ForeignKey(User, related_name='equipment_employee', on_delete=models.SET_NULL, null=True,
                                 blank=True)
    location = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True)
    counter = models.IntegerField(blank=True, null=True)

    def store(self, stock_id: int = None, condition_id: int = None) -> 'Equipment':
        """Stores the equipment at a stock location. By default the equipment is returned to it's
        original location. If a stock_id is supplied the equipment is moved to a new equipment location with
        the given stock_id """
        if condition_id:
            self.condition = Condition.objects.get(pk=condition_id)
        if not self.condition.is_storable:
            raise ProductConditionError(_(f'This equipment in condition {self.condition} cannot be stored'))
        if not stock_id and not self.stock_id:
            raise StockLogicError(
                _('the current equipment does not have a inventory associated with it. A inventory_id must be '
                  'passed'))
        if self.status == self.Status.STORED and self.stock_id and stock_id and int(self.stock_id) == int(stock_id):
            raise StockLogicError(_('cannot store stock item in a location it is already stored in'))
        self.stock_id = stock_id or self.stock_id
        self.employee = None
        self.status = self.Status.STORED
        return self.save()

    def pickup(self, employee_id: int, condition_id: int = None) -> 'EquipmentTransaction':
        """Product is picked up from a customer location or a inventory location. An employee is assigned to the
        equipment. """
        if condition_id:
            self.condition = Condition.objects.get(pk=condition_id)
        self.employee.id = employee_id
        self.status = self.Status.PICKED_UP
        equipment_transaction = EquipmentTransaction(equipment=self,
            transaction_type=EquipmentTransaction.TransactionType.PICK_UP, condition=self.condition,
            employee=self.employee)
        with transaction.atomic():
            #order_equipment.save()
            equipment_transaction.save()
            self.save()
        return self.save()

    def deploy(self, order_id: int, condition_id: int = None) -> 'EquipmentTransaction':
        """Deploys the equipment at a customer location"""
        if self.status != self.Status.PICKED_UP:
            raise ProductStatusError(_('item must be picked up before it can be deployed'))
        if condition_id:
            self.condition = Condition.objects.get(pk=condition_id)
        if not self.condition.is_deployable:
            raise ProductConditionError(_(f'{self.condition} item cannot be deployed'))
        self.status = self.Status.DEPLOYED
        order_equipment = OrderEquipment(equipment=self, order_id=order_id, deployed=timezone.now(), )
        equipment_transaction = EquipmentTransaction.objects.create(equipment=self,
            transaction_type=EquipmentTransaction.TransactionType.DEPLOY, condition=self.condition,
            employee=self.employee)
        with transaction.atomic():
            order_equipment.save()
            equipment_transaction.save()
            self.save()
        return equipment_transaction

    def transfer(self, employee_id: int, condition_id: int = None) -> 'Equipment':
        """Transfers equipment from one employee to another"""
        if condition_id:
            self.condition = Condition.objects.get(pk=condition_id)
        if employee_id == self.employee.id:
            raise TransactionError("Cannot transfer equipment to the current equipment holder")
        self.employee.id = employee_id
        EquipmentTransaction.objects.create(equipment=self,
                                            transaction_type=EquipmentTransaction.TransactionType.TRANSFER,
                                            condition=self.condition, employee=self.employee)
        return self.save()

    def decommission(self) -> 'Equipment':
        """Decommissions the item and removes all employee, inventory, and location associations"""
        self.employee = None
        self.stock = None
        self.status = self.Status.DECOMMISSIONED
        EquipmentTransaction.objects.create(equipment=self,
                                            transaction_type=EquipmentTransaction.TransactionType.DECOMMISSION,
                                            condition=self.condition, employee=self.employee)
        return self.save()

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Equipment')
        verbose_name_plural = _('Equipment')

    def get_absolute_url(self):
        return reverse_lazy('inventory:equipment_detail', kwargs={'pk': self.pk})

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # TODO  Review This Method for uniqueness and usefulness
        if not self.name:
            self.name = self.name or slugify(
                f'{self.product.generic_product.name} {self.product.id} {self.product.counter}')
            self.counter = self.product.counter
            self.product.counter += 1
            self.product.save()
        return super().save(force_insert, force_update, using, update_fields)


class Condition(models.Model):
    """Physical condition of the product that determines if it can be used"""
    name = models.CharField(verbose_name=_('name'), max_length=32)
    description = models.TextField(verbose_name=_('description'))
    is_deployable = models.BooleanField(verbose_name=_('is deployable'), default=False)
    is_storable = models.BooleanField(verbose_name=_('is storable'), default=False)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Condition')
        verbose_name_plural = _('Conditions')


class EquipmentTransaction(models.Model):
    class TransactionType(models.TextChoices):
        STORE = 'Store', _('Store')
        PICK_UP = 'Pick_Up', _('Pick Up')
        DEPLOY = _('Deploy')
        TRANSFER = _('Transfer')
        WITHDRAW = _('Withdraw')
        DECOMMISSION = _('Decommission')

    equipment = models.ForeignKey('Equipment', verbose_name=_('equipment'), on_delete=models.PROTECT)
    transaction_type = models.CharField(verbose_name=_('type'), max_length=32, choices=TransactionType.choices)
    employee = models.ForeignKey(User, verbose_name=_('employee'), on_delete=models.PROTECT)
    condition = models.ForeignKey('Condition', verbose_name=_('condition'), on_delete=models.PROTECT)
    timestamp = models.DateTimeField(verbose_name=_('timestamp'), auto_now=True)

    def __str__(self):
        return f'{self.transaction_type} {self.equipment} at {self.timestamp} by {self.employee}'

    class Meta:
        verbose_name = _('Equipment Transaction')
        verbose_name_plural = _('Equipment Transactions')
