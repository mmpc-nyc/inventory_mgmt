from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class Vendor(models.Model):
    """A person, company, or organization that sells goods."""
    name = models.CharField(max_length=150, blank=True)
    active = models.BooleanField(default=True)
    delivery_time = models.PositiveIntegerField()
    website = models.URLField(max_length=256, default='', blank=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Vendor')
        verbose_name_plural = _('Vendors')

    def get_absolute_url(self):
        return reverse_lazy('warehouse:vendor_detail', kwargs={'pk': self.pk})


class VendorMaterial(models.Model):
    """good or service that is produced or supplied by an external vendor or supplier,
    rather than being produced in-house. It is offered for sale by the vendor."""
    material = models.ForeignKey('Material', on_delete=models.CASCADE)
    sku = models.CharField(max_length=256)



