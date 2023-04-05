from datetime import timedelta

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from common.models.field import Field


class Equipment(models.Model):
    """
    Equipment refers to tracked physical assets such as machinery and tools used in a business, that are not vehicles and are
    tracked for inventory purposes. These assets are depreciable and can be used to generate income or are necessary for production.
    """

    class AssetType(models.TextChoices):
        SHORT_TERM = 'Short Term', _('Short Term')
        LONG_TERM = 'Long Term', _('Long Term')

    name = models.CharField(max_length=150, blank=True, null=True)
    category = TreeForeignKey('EquipmentCategory', on_delete=models.SET_NULL, null=True, blank=True)
    equipment_class = models.ForeignKey('inventory.EquipmentClass', on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.ForeignKey('inventory.Brand', on_delete=models.CASCADE)
    warranty_days = models.IntegerField(blank=True, null=True)
    asset_type = models.CharField(choices=AssetType.choices, max_length=20, default=AssetType.SHORT_TERM)


    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Equipment')
        verbose_name_plural = _('Equipment')

    def get_absolute_url(self):
        return reverse_lazy('inventory:equipment_detail', kwargs={'pk': self.pk})


class EquipmentItem(models.Model):
    """
    Represents a physical piece of equipment.
    """

    class Status(models.TextChoices):
        """Current status of the material"""

        STORED = 'STORED', _('Stored')  # Equipment stored in Stock Location
        DEPLOYED = 'DEPLOYED', _('Deployed')  # Equipment is currently deployed at order location
        PICKED_UP = 'PICKED_UP', _('Picked Up')  # Equipment is with the employee
        MISSING = 'MISSING', _('Missing')  # Equipment cannot be found.
        DECOMMISSIONED = 'DECOMMISSIONED', _('Decommissioned')

    equipment = models.ForeignKey('inventory.Equipment', on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=50, unique=True)
    purchase_date = models.DateField(null=True, blank=True, default=timezone.now())
    purchase_price = models.DecimalField(decimal_places=2, max_digits=8, default=0)
    purchase_from = models.ForeignKey('inventory.Vendor', blank=True, null=True, on_delete=models.SET_NULL)
    purchased_by = models.ForeignKey('users.User', on_delete=models.CASCADE)
    status = models.CharField(max_length=32, choices=Status.choices, default=Status.STORED)
    stock_location = models.ForeignKey('inventory.StockLocation', on_delete=models.SET_NULL, blank=True, null=True)
    condition = models.ForeignKey('Condition', on_delete=models.CASCADE, default=1)
    notes = models.TextField(blank=True)
    warranty_expiration_date = models.DateField(null=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        if self.purchase_date and self.equipment.warranty_days:
            self.warranty_expiration_date = self.purchase_date + timedelta(days=self.equipment.warranty_days)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.equipment.name} ({self.serial_number})"

    class Meta:
        verbose_name = _('Equipment Item')
        verbose_name_plural = _('Equipment Items')


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

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Condition')
        verbose_name_plural = _('Conditions')
