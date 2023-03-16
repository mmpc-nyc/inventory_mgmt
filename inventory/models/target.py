from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Target(MPTTModel):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'{self.name} | {self.content_object}'

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
