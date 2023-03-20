from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.utils.translation import gettext_lazy as _


class Target(MPTTModel):
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=256)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Target')
        verbose_name_plural = _('Targets')
