from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from common.models.address import Address


class StockLocation(models.Model):
    """A holder for all equipment"""

    class StockLocationStatus(models.TextChoices):
        """Choices for setting the status of a stock_location location
        Active: Available for picking up and dropping off items
        Inactive: Not in use. Materials cannot be picked up or dropped off from this location
        Full: The inventory location is currently full. No items can be dropped off.
        """

        ACTIVE = 'Active', _('Active')
        INACTIVE = 'Inactive', _('Inactive')
        FULL = 'Full', _('Full')

    name = models.CharField(max_length=150, blank=True)
    status = models.CharField(max_length=32, choices=StockLocationStatus.choices, default=StockLocationStatus.ACTIVE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Stock Location')
        verbose_name_plural = _('Stock Locations')

    def get_absolute_url(self):
        return reverse_lazy('stock_location:stock_location_detail', kwargs={'pk': self.pk})


class MaterialStock(models.Model):
    """
    Represents the stock of a material at a particular stock location.
    """
    material = models.ForeignKey('inventory.Material', on_delete=models.CASCADE)
    stock_location = models.ForeignKey(StockLocation, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    min_quantity = models.PositiveIntegerField(default=0)
    max_quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.material.name} @ {self.stock_location.name}"

    class Meta:
        verbose_name = _('Material Stock')
        verbose_name_plural = _('Material Stocks')
        unique_together = ['material', 'stock_location']
