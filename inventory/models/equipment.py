from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from inventory.exceptions import ProductConditionError, StockLogicError, ProductOrderAssignmentError, ProductStatusError


class Equipment(models.Model):
    # TODO  Write Description

    class Condition(models.TextChoices):
        """Physical condition of the product that determines if it can be used"""

        WORKING = 'WORKING', _('Working')  # Equipment is in good working condition
        DAMAGED = 'DAMAGED', _('Damaged')  # Equipment is damaged and needs repair
        DECOMMISSIONED = 'DECOMMISSIONED', _('Decommissioned')  # Unusable equipment that cannot be repaired.

        _usable_conditions: set = {WORKING, }
        _storable_conditions: set = {WORKING, DAMAGED}

        @classmethod
        def deployable(cls, condition: str) -> bool:
            return condition in cls._usable_conditions

        @classmethod
        def storable(cls, condition: str) -> bool:
            return condition in cls._storable_conditions

    class Status(models.TextChoices):
        """Current status of the product"""

        STORED = 'STORED', _('Stocked')  # Equipment stored in Stock
        DEPLOYED = 'DEPLOYED', _('Deployed')  # Equipment is currently deployed a order location
        PICKED_UP = 'PICKED_UP', _('Picked Up')  # Equipment is with the employee

    name = models.CharField(max_length=150, blank=True, null=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.STORED)
    condition = models.CharField(max_length=48, choices=Condition.choices, default=Condition.WORKING)
    stock = models.ForeignKey('Stock', on_delete=models.SET_NULL, blank=True, null=True)
    employee = models.ForeignKey(get_user_model(), related_name='product_employee', on_delete=models.SET_NULL,
                                 null=True, blank=True)
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True, blank=True)
    counter = models.IntegerField(blank=True, null=True)
    history = HistoricalRecords()

    def store(self, stock_id: int = None) -> 'Equipment':
        """Stores the equipment at a stock location. By default the equipment is returned to it's
        original location. If a stock_id is supplied the equipment is moved to a new equipment location with
        the given stock_id """
        if not self.Condition.storable(self.condition):
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

    def pickup(self, employee_id: int) -> 'Equipment':
        """Product is picked up from a customer location or a inventory location. An employee is assigned to the
        equipment. """
        if self.employee_id == employee_id:
            raise StockLogicError(_('the same user cannot pick up an equipment they are already holding'))
        self.employee_id = employee_id
        self.status = self.Status.PICKED_UP
        return self.save()

    def deploy(self, order_id: int = None) -> 'Equipment':
        if not order_id and not self.order:
            raise ProductOrderAssignmentError(_('A order must be assigned to deploy the product'))
        self.order = order_id or self.order
        """Deploys the equipment at a customer location"""
        if self.status == self.Condition.deployable(self.condition):
            raise ProductStatusError(_('decommissioned equipment cannot be deployed'))
        if self.status != self.Status.PICKED_UP:
            raise ProductStatusError(_('item must be picked up before it can be deployed'))
        if self.condition in self.Condition.DAMAGED or self.Condition.DECOMMISSIONED:
            raise ProductConditionError(_('broken or irreparable item cannot be deployed'))
        self.status = self.Status.DEPLOYED
        return self.save()

    def decommission(self) -> 'Equipment':
        """Decommissions the item and removes all employee, inventory, and location associations"""
        notification_message: str = ''  # TODO  Add notification message for decommissioning an item.
        self.employee = None
        self.stock = None
        self.status = self.Status.DECOMMISSIONED
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
            self.name = slugify(f'{self.product.generic_product.name} {self.product.id} {self.product.counter}')
            self.counter = self.product.counter
            self.product.counter += 1
            self.product.save()
        return super().save(force_insert, force_update, using, update_fields)