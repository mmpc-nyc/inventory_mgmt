from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from inventory.exceptions import OrderCompletionError
from inventory.models import Customer, Location, Equipment


class Order(models.Model):
    """Model for scheduling orders to allow easier assignment of inventory, services and products"""

    class Activity(models.TextChoices):
        DEPLOY = 'Deploy', _('Deploy')
        PICKUP = 'Pickup', _('Pickup')
        INSPECT = 'Inspect', _('Inspect')

    class Status(models.TextChoices):
        NEW = 'New', _('New')
        ASSIGNED = 'Assigned', _('Assigned')
        ACTIVE = 'Active', _('Active')
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

    def missing_equipment_check(self, mark_deployed_as_missing):
        """If there is any equipment that is still deployed the completion will fail unless the
        "mark_deployed_as_missing" is true then the status of the remaining deployed equipment will
        be set to MISSING"""

        deployed_equipment = self.get_deployed_equipment()
        if deployed_equipment:
            if not mark_deployed_as_missing:
                raise OrderCompletionError('Not all equipment has been picked up')
            deployed_equipment.update(status=Equipment.Status.MISSING)

    def complete(self, mark_deployed_as_missing: bool = False):
        """Completes the order"""
        self.missing_equipment_check(mark_deployed_as_missing=mark_deployed_as_missing)
        self.status = self.Status.COMPLETED
        self.save()

    def _complete_deploy_order(self):
        ...

    def _complete_pickup_order(self):
        ...

    def _complete_inspection_order(self):
        ...

    def cancel(self, mark_deployed_as_missing: bool = False):
        """Cancels the order"""
        self.missing_equipment_check(mark_deployed_as_missing=mark_deployed_as_missing)
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

    def __str__(self):
        return f'{self.order} | {self.equipment}'

    class Meta:
        verbose_name = _('Order Equipment')
        verbose_name_plural = _('Order Equipment')
        unique_together = ('order', 'equipment')
