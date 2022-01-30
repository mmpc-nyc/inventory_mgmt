from django.db import models
from django.urls import reverse_lazy
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Product(models.Model):
    """A unique identifier for a product consisting of name, brand, product type, and generic product"""

    class Status(models.TextChoices):
        """Product status choices
        TODO  Rethink this
        """
        ACTIVE = 'Active', _('Active')  # Can be used and allows purchasing of new equipment
        INACTIVE = 'Inactive', _('Inactive')  # The product is no longer active but is still stored in the inventory
        RECALL = 'Recall', _('Recall')  # The product is inactive and should no longer be used.

    name = models.CharField(max_length=150)
    generic_product = models.ForeignKey('GenericProduct', on_delete=models.CASCADE)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.ACTIVE)
    counter = models.IntegerField(default=0)

    @cached_property
    def count(self):
        return self.equipment_set.count()

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


class GenericProduct(models.Model):
    """A generic product container that relates to different versions of the same product.
    For example: a product having different brands or different sizes or colors
    """

    class Status(models.TextChoices):
        """Generic Product status choices
        Active: The generic product is available for all actions
        Inactive: The generic product is no longer active but is still stored in the inventory
        """
        ACTIVE = 'Active', _('Active')
        INACTIVE = 'Inactive', _('Inactive')

    category = TreeForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=150, unique=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.ACTIVE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Generic Product')
        verbose_name_plural = _('Generic Products')


class Category(MPTTModel):
    name = models.CharField(max_length=64)
    slug = models.SlugField()
    parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    class MPTTMeta:
        order_insertion_by = ['name', ]

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return f'{self.name}'