from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from inventory.exceptions import ProductConditionError, StockLogicError, ProductOrderAssignmentError, \
    ProductStatusError, TransactionError

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

    def pickup(self, employee_id: int, condition_id: int = None) -> 'Equipment':
        """Product is picked up from a customer location or a inventory location. An employee is assigned to the
        equipment. """
        if condition_id:
            self.condition = Condition.objects.get(pk=condition_id)
        self.employee.id = employee_id
        self.status = self.Status.PICKED_UP
        EquipmentTransaction.objects.create(
            equipment=self,
            transaction_type=EquipmentTransaction.TransactionType.PICK_UP,
            condition=self.condition,
            employee=self.employee
        )
        return self.save()

    def deploy(self, order_id: int = None, condition_id: int = None) -> 'Equipment':
        """Deploys the equipment at a customer location"""
        if condition_id:
            self.condition = Condition.objects.get(pk=condition_id)
        if not order_id and not self.order:
            raise ProductOrderAssignmentError(_('A order must be assigned to deploy the product'))
        self.order = order_id or self.order
        if self.status != self.Status.PICKED_UP:
            raise ProductStatusError(_('item must be picked up before it can be deployed'))
        if not self.condition.is_deployable:
            raise ProductConditionError(_(f'{self.condition} item cannot be deployed'))
        self.status = self.Status.DEPLOYED
        EquipmentTransaction.objects.create(
            equipment=self,
            transaction_type=EquipmentTransaction.TransactionType.DEPLOY,
            condition=self.condition,
            employee=self.employee
        )
        return self.save()

    def transfer(self, employee_id: int, condition_id: int = None) -> 'Equipment':
        """Transfers equipment from one employee to another"""
        if condition_id:
            self.condition = Condition.objects.get(pk=condition_id)
        if employee_id == self.employee.id:
            raise TransactionError("Cannot transfer equipment to the current equipment holder")
        self.employee.id = employee_id
        EquipmentTransaction.objects.create(
            equipment=self,
            transaction_type=EquipmentTransaction.TransactionType.TRANSFER,
            condition=self.condition,
            employee=self.employee
        )
        return self.save()

    def decommission(self) -> 'Equipment':
        """Decommissions the item and removes all employee, inventory, and location associations"""
        self.employee = None
        self.stock = None
        self.status = self.Status.DECOMMISSIONED
        EquipmentTransaction.objects.create(
            equipment=self,
            transaction_type=EquipmentTransaction.TransactionType.DECOMMISSION,
            condition=self.condition,
            employee=self.employee
        )
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
            self.name = self.name or slugify(f'{self.product.generic_product.name} {self.product.id} {self.product.counter}')
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
        STORE = _('Store')
        PICK_UP = _('Pick Up')
        DEPLOY = _('Deploy')
        TRANSFER = _('Transfer')
        DECOMMISSION = _('Decommission')

    equipment = models.ForeignKey('Equipment', verbose_name=_('equipment'), on_delete=models.PROTECT)
    transaction_type = models.CharField(verbose_name=_('type'), max_length=32, choices=TransactionType.choices)
    employee = models.ForeignKey(User, verbose_name=_('employee'), on_delete=models.PROTECT)
    condition = models.ForeignKey('Condition', verbose_name=_('condition'), on_delete=models.PROTECT)
    timestamp = models.DateTimeField( verbose_name=_('timestamp'),auto_created=True)

    def __str__(self):
        return f'{self.transaction_type} {self.equipment} at {self.timestamp} by {self.employee}'

    class Meta:
        verbose_name = _('Equipment Transaction')
        verbose_name_plural = _('Equipment Transactions')
