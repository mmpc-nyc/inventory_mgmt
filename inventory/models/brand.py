from django.db import models
from django.utils.translation import gettext_lazy as _


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