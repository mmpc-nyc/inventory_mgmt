from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from common.models.field import Field
from inventory.models.unit import Unit
from inventory.models.vendor import Vendor


class MaterialCategory(MPTTModel):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    fields = GenericRelation(Field)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    class MPTTMeta:
        order_insertion_by = ['name', ]

    class Meta:
        verbose_name = _('Material Category')
        verbose_name_plural = _('Material Categories')

    def __str__(self):
        return f'{self.name}'


class MaterialClass(models.Model):
    #  TODO  Write Description
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Material Class')
        verbose_name_plural = _('Material Classes')


class Material(models.Model):
    """A unique identifier for a material consisting of name, brand, material type"""

    name = models.CharField(max_length=150)
    description = models.TextField()
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    material_class = models.ForeignKey('MaterialClass', verbose_name='type', on_delete=models.SET_NULL, null=True)
    category = TreeForeignKey('MaterialCategory', on_delete=models.SET_NULL, null=True, blank=True)
    is_taxable = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_product = models.BooleanField(default=False)
    product_sell_price = models.DecimalField(decimal_places=2, max_digits=8, default=0)
    material_sell_price = models.DecimalField(decimal_places=2, max_digits=8, default=0)
    preferred_vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, blank=True, null=True)
    usage_unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='usage_unit')
    retail_unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='retail_unit')
    min_stock = models.PositiveIntegerField(default=0)
    max_stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.name} | {self.brand.name}'

    class Meta:
        verbose_name = _('Material')
        verbose_name_plural = _('Materials')

    def get_absolute_url(self):
        return reverse_lazy('inventory:material_detail', kwargs={'pk': self.pk})


class MaterialField(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.field.name}: {self.value}"


class Brand(models.Model):
    #  TODO  Write Description
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')
