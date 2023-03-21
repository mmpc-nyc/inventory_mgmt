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
    location = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Stock Location')
        verbose_name_plural = _('Stock Locations')

    def get_absolute_url(self):
        return reverse_lazy('stock_location:stock_location_detail', kwargs={'pk': self.pk})