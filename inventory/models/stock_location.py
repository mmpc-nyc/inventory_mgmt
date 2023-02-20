from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from inventory.models.location import Location


class StockLocation(models.Model):
    """A holder for all equipment"""

    class StockLocationStatus(models.TextChoices):
        """Choices for setting the status of a warehouse location
        Active: Available for picking up and dropping off items
        Inactive: Not in use. Products cannot be picked up or dropped off from this location
        Full: The inventory location is currently full. No items can be dropped off.
        """

        ACTIVE = 'Active', _('Active')
        INACTIVE = 'Inactive', _('Inactive')
        FULL = 'Full', _('Full')

    name = models.CharField(max_length=150, blank=True)
    status = models.CharField(max_length=32, choices=StockLocationStatus.choices, default=StockLocationStatus.ACTIVE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('StockLocation')
        verbose_name_plural = _('StockLocations')

    def get_absolute_url(self):
        return reverse_lazy('warehouse:warehouse_detail', kwargs={'pk': self.pk})