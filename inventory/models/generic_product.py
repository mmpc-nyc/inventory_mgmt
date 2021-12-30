from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from simple_history.models import HistoricalRecords


class GenericProduct(models.Model):
    """A generic product container that relates to different versions of the same product.
    For example: a product having different brands or different sizes or colors
    """

    class Status(models.TextChoices):
        """Product status choices
        Stored: Product stored in Stock
        Deployed: Product deployed at customer location
        Decommissioned: Product no longer in use and not in inventory
        Inactive: The product is no longer active but is still stored in the inventory
        Recall: The product is inactive and should no longer be used.
        Picked Up: Product is currently with the employee. Not at any customer location or inventory.
        """
        ACTIVE = 'ACTIVE', _('Active')
        INACTIVE = 'INACTIVE', _('Inactive')
        RECALL = 'RECALL', _('Recall')

    category = TreeForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=150, unique=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.ACTIVE)
    history = HistoricalRecords()

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