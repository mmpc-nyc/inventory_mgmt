from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Target(MPTTModel):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    materials = models.ManyToManyField('Material', related_name='target_materials')
    equipments = models.ManyToManyField('Equipment', related_name='target_equipments')
    services = models.ManyToManyField('Service', related_name='target_services')



    def __str__(self):
        return f'{self.name}'