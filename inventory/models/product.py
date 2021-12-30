from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from inventory.models.equipment import Equipment


class Product(models.Model):
    """TODO  Write Description"""

    class Status(models.TextChoices):
        """Product status choices
        TODO  Rethink this
        """
        ACTIVE = 'ACTIVE', _('Active')  # Can be used and allows purchasing of new equipment
        INACTIVE = 'INACTIVE', _('Inactive')  # The product is no longer active but is still stored in the inventory
        RECALL = 'RECALL', _('Recall')  # The product is inactive and should no longer be used.

    name = models.CharField(max_length=150)
    generic_product = models.ForeignKey('GenericProduct', on_delete=models.PROTECT)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    product_type = models.ForeignKey('ProductType', on_delete=models.CASCADE)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.ACTIVE)
    counter = models.IntegerField(default=0)

    @property
    def count(self):
        return self.equipment_set.count()

    @property
    def stored_count(self):
        return self.equipment_set.filter(status=Equipment.Status.STORED).quantity()

    @property
    def deployed_count(self):
        return self.equipment_set.filter(status=Equipment.Status.DEPLOYED).quantity()

    @property
    def picked_up_count(self):
        return self.equipment_set.filter(status=Equipment.Status.PICKED_UP).quantity()

    def __str__(self):
        return f'{self.name} | {self.brand.name}'

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def get_absolute_url(self):
        return reverse_lazy('inventory:product_detail', kwargs={'pk': self.pk})


class ProductType(models.Model):
    #  TODO  Write Description
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Product Type')
        verbose_name_plural = _('Product Types')


class Brand(models.Model):
    #  TODO  Write Description
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')
