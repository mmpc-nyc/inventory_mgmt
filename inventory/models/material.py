from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from common.models.field import Field
from inventory.models.target import Target
from inventory.models.unit import Unit
from inventory.models.vendor import Vendor


class Material(models.Model):
    """
    Represents a material or product that can be sold, purchased, or used by the organization.
    """

    name = models.CharField(max_length=150)
    description = models.TextField()
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    material_class = models.ForeignKey('MaterialClass', verbose_name='class', on_delete=models.SET_NULL, null=True)
    category = TreeForeignKey('MaterialCategory', on_delete=models.SET_NULL, null=True, blank=True)
    targets = GenericRelation(Target)
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


class MaterialCategory(MPTTModel):
    """
    Represents a category of materials that share common fields, properties, or characteristics.
    """
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
    """
    Represents a category of materials that can be used interchangeably based on their
    properties or intended use, allowing them to be grouped together for easy access.
    """

    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Material Class')
        verbose_name_plural = _('Material Classes')


class MaterialField(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.field.name}: {self.value}"


class Brand(models.Model):
    """
    Represents a brand or manufacturer of products.
    """
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')
