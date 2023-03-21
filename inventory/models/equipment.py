from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from common.models.field import Field


class Equipment(models.Model):
    """Equipment refers to tracked physical assets such as machinery and tools used in a business, that are not vehicles and are tracked for inventory purposes. These assets are depreciable and can be used to generate income or are necessary for production. The inventory tracking system maintains their quantity, location, status, maintenance and other relevant information."""

    class Status(models.TextChoices):
        """Current status of the material"""

        STORED = 'STORED', _('Stored')  # Equipment stored in Stock Location
        DEPLOYED = 'DEPLOYED', _('Deployed')  # Equipment is currently deployed at order location
        PICKED_UP = 'PICKED_UP', _('Picked Up')  # Equipment is with the employee
        MISSING = 'MISSING', _('Missing')  # Equipment cannot be found.
        DECOMMISSIONED = 'DECOMMISSIONED', _('Decommissioned')

    name = models.CharField(max_length=150, blank=True, null=True)
    status = models.CharField(max_length=32, choices=Status.choices, default=Status.STORED)
    stock_location = models.ForeignKey('inventory.StockLocation', on_delete=models.SET_NULL, blank=True, null=True)
    condition = models.ForeignKey('Condition', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), related_name='equipment_employee', on_delete=models.SET_NULL, null=True,
                             blank=True)
    category = TreeForeignKey('EquipmentCategory', on_delete=models.SET_NULL, null=True, blank=True)
    equipment_class = models.ForeignKey('inventory.EquipmentClass', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Equipment')
        verbose_name_plural = _('Equipment')

    def get_absolute_url(self):
        return reverse_lazy('inventory:equipment_detail', kwargs={'pk': self.pk})


class EquipmentItem(models.Model):
    """
    Represents an individual instance of a piece of equipment.
    """
    equipment = models.ForeignKey('inventory.Equipment', on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=50, unique=True)
    purchase_date = models.DateField(null=True, blank=True)
    purchase_price = models.DecimalField(decimal_places=2, max_digits=8, default=0)
    current_value = models.DecimalField(decimal_places=2, max_digits=8, default=0)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.equipment.name} ({self.serial_number})"


class EquipmentClass(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Equipment Class')
        verbose_name_plural = _('Equipment Classes')


class EquipmentCategory(MPTTModel):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    fields = GenericRelation(Field)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    class MPTTMeta:
        order_insertion_by = ['name', ]

    class Meta:
        verbose_name = _('Equipment Category')
        verbose_name_plural = _('Equipment Categories')

    def __str__(self):
        return f'{self.name}'


class EquipmentField(models.Model):
    material = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.field.name}: {self.value}"


class Condition(models.Model):
    """Physical condition of the material that determines if it can be used"""
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
