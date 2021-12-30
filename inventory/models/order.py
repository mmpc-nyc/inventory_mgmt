from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from inventory.models import Customer, Location


class Order(models.Model):
    """Model for scheduling orders to allow easier assignment of inventory, services and products"""

    class Status(models.TextChoices):
        NEW = 'NEW', _('New')
        ASSIGNED = 'ASSIGNED', _('Assigned')
        ACTIVE = 'ACTIVE', _('Active')
        COMPLETED = 'COMPLETED', _('Completed')
        CANCELED = 'CANCELED', _('Canceled')

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.NEW)
    employees = models.ManyToManyField(get_user_model(), related_name='order_employees')
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    date = models.DateTimeField()
    history = HistoricalRecords()
    generic_products = models.ManyToManyField('GenericProduct', through='OrderGenericProduct',
                                              related_name='generic_products')

    def complete(self):
        """Completes the order"""
        #  TODO  Implement this function
        ...

    def cancel(self):
        """Cancels the order"""
        #  TODO  Implement this function
        ...

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
