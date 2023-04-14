from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from common.models.address import Address


class StorageLocation(models.Model):
    """A holder for all equipment"""

    name = models.CharField(max_length=150, blank=True)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    description = models.TextField()
    access_monday_start = models.TimeField(null=True, blank=True)
    access_monday_end = models.TimeField(null=True, blank=True)
    access_tuesday_start = models.TimeField(null=True, blank=True)
    access_tuesday_end = models.TimeField(null=True, blank=True)
    access_wednesday_start = models.TimeField(null=True, blank=True)
    access_wednesday_end = models.TimeField(null=True, blank=True)
    access_thursday_start = models.TimeField(null=True, blank=True)
    access_thursday_end = models.TimeField(null=True, blank=True)
    access_friday_start = models.TimeField(null=True, blank=True)
    access_friday_end = models.TimeField(null=True, blank=True)
    access_saturday_start = models.TimeField(null=True, blank=True)
    access_saturday_end = models.TimeField(null=True, blank=True)
    access_sunday_start = models.TimeField(null=True, blank=True)
    access_sunday_end = models.TimeField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Storage Location')
        verbose_name_plural = _('Storage Locations')

    def get_absolute_url(self):
        return reverse_lazy('storage_location:storage_location_detail', kwargs={'pk': self.pk})


class MaterialStock(models.Model):
    """
    Represents the stock of a material at a particular stock location.
    """
    material = models.ForeignKey('inventory.Material', on_delete=models.CASCADE)
    storage_location = models.ForeignKey(StorageLocation, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    min_quantity = models.PositiveIntegerField(default=0)
    max_quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.material.name} @ {self.storage_location.name}"

    class Meta:
        verbose_name = _('Material Stock')
        verbose_name_plural = _('Material Stocks')
        unique_together = ['material', 'storage_location']
