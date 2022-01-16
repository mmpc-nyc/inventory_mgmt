from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from inventory.exceptions import ProductConditionError
from inventory.models.product import Product
from inventory.models.stock import Stock


class Equipment(models.Model):
    """A product that is can be stored, deployed, and picked up. """

    class Status(models.TextChoices):
        """Current status of the product"""

        STORED = 'STORED', _('Stored')  # Equipment stored in Stock
        DEPLOYED = 'DEPLOYED', _('Deployed')  # Equipment is currently deployed at order location
        PICKED_UP = 'PICKED_UP', _('Picked Up')  # Equipment is with the employee
        MISSING = 'MISSING', _('Missing')  # Equipment cannot be found.
        DECOMMISSIONED = 'DECOMMISSIONED', _('Decommissioned')

    name = models.CharField(max_length=150, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField(max_length=32, choices=Status.choices, default=Status.STORED)
    stock = models.ForeignKey('Stock', on_delete=models.SET_NULL, blank=True, null=True)
    condition = models.ForeignKey('Condition', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), related_name='equipment_employee', on_delete=models.SET_NULL, null=True,
                             blank=True)
    location = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True, blank=True)
    counter = models.IntegerField(blank=True, null=True)

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
                 condition: 'Condition' = None, stock: 'Stock' = None,
                 recipient: get_user_model() = None) -> 'EquipmentTransaction':
        if not self.condition.has_action(action.name):
            raise ProductConditionError(_(f'This equipment in condition {self.condition} cannot use action {action}'))

        with transaction.atomic():
            self.save()
            stock = stock or self.stock
            condition = condition or self.condition
            return EquipmentTransaction.objects.create(action=action, equipment=self, user=user, condition=condition,
                                                       stock=stock, order=order, recipient=recipient)

    def decommission(self, user: get_user_model()):
        action = EquipmentTransactionAction.DECOMMISSION
        condition = Condition.objects.get(name='Decommissioned')

        self.user = None
        self.status = self.Status.DECOMMISSIONED
        self.location = None
        self.stock = None
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

    def store(self, user: get_user_model(), stock: 'Stock' = None, condition: 'Condition' = None):
        action = EquipmentTransactionAction.STORE
        stock = stock or self.stock

        self.user = None
        self.location = stock.location
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


class EquipmentTransaction(models.Model):
    """A model for managing equipment transactions. Mainly used for logging and auditing"""
    action = models.CharField(max_length=32, choices=EquipmentTransactionAction.choices)
    equipment = models.ForeignKey(Equipment, verbose_name=_('equipment'), on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), verbose_name=_('user'), on_delete=models.CASCADE)
    recipient = models.ForeignKey(get_user_model(), verbose_name=_('recipient'), related_name='recipient',
                                  on_delete=models.CASCADE, blank=True, null=True)
    stock = models.ForeignKey('Stock', verbose_name=_('stock'), on_delete=models.CASCADE, blank=True, null=True)
    condition = models.ForeignKey(Condition, verbose_name=_('condition'), on_delete=models.CASCADE)
    timestamp = models.DateTimeField(verbose_name=_('timestamp'), auto_now=True)
    location = models.ForeignKey('Location', verbose_name=_('Location'), blank=True, null=True,
                                 on_delete=models.CASCADE)
    order = models.ForeignKey('Order', verbose_name=_('Order'), blank=True, null=True, on_delete=models.CASCADE)

    def clean(self):
        super().clean()

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = _('Equipment Transaction')
        verbose_name_plural = _('Equipment Transactions')
