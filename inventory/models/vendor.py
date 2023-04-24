from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class Vendor(models.Model):
    """A person, company, or organization that sells goods."""
    name = models.CharField(max_length=150, blank=True)
    delivery_time = models.PositiveIntegerField(default=7, blank=True)
    website = models.URLField(max_length=256, default='', blank=True)
    contact = models.ForeignKey('common.Contact', blank=True, null=True, on_delete=models.SET_NULL)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Vendor')
        verbose_name_plural = _('Vendors')


class VendorItem(models.Model):
    sku = models.CharField(max_length=256, verbose_name=_('SKU'))
    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_('unit price'))
    promo_unit_price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_('promotional unit price'),
                                           blank=True, null=True)
    promo_start_date = models.DateField(blank=True, null=True, verbose_name=_('promotion start date'))
    promo_end_date = models.DateField(blank=True, null=True, verbose_name=_('promotion end date'))
    delivery_time = models.PositiveIntegerField(default=7, blank=True)
    is_taxed = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)

    @property
    def current_price(self):
        current_date = timezone.now().date()
        if self.promo_start_date and self.promo_end_date and self.promo_start_date <= current_date <= self.promo_end_date:
            return self.promo_unit_price
        else:
            return self.unit_price

    class Meta:
        abstract = True


class VendorMaterial(VendorItem):
    """A good or service that is produced or supplied by an external vendor or supplier,
    rather than being produced in-house. It is offered for sale by the vendor."""

    material = models.ForeignKey('inventory.Material', on_delete=models.CASCADE, verbose_name=_('material'))

    def __str__(self):
        return f'{self.material.name} ({self.sku})'

    class Meta:
        verbose_name = _('Vendor Material')
        verbose_name_plural = _('Vendor Materials')


class VendorEquipment(VendorItem):
    """Equipment that is produced or supplied by an external vendor or supplier,
    rather than being produced in-house. It is offered for sale by the vendor."""

    equipment = models.ForeignKey('inventory.Material', on_delete=models.CASCADE, verbose_name=_('material'))

    def __str__(self):
        return f'{self.equipment.name} ({self.sku})'

    class Meta:
        verbose_name = _('Vendor Equipment')
        verbose_name_plural = _('Vendor Equipment')
