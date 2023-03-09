from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _


class Field(models.Model):
    class FieldType(models.TextChoices):
        TEXT_FIELD = 'TEXT_FIELD', _('Text Field')
        TEXT_AREA = 'TEXT_AREA', _('Text Area')
        SELECT = 'SELECT', _('Select')
        DATETIME = 'DATETIME', _('Datetime')
        DATE = 'DATE', _('Date')
        MULTIPLE_SELECT = 'MULTIPLE_SELECT', _('Multiple Select')
        INTEGER = 'INTEGER', _('Integer')
        FLOAT = 'FLOAT', _('Float')
        BOOLEAN = 'BOOLEAN', _('Boolean')

    class ValidationType(models.TextChoices):
        NONE = 'NONE', _('None')
        RANGE = 'RANGE', _('Range')
        REGEX = 'REGEX', _('Regular Expression')
        EMAIL = 'EMAIL', _('Email Address')
        URL = 'URL', _('URL')
        NUMERIC = 'NUMERIC', _('Numeric Value')
        INTEGER = 'INTEGER', _('Integer Value')
        BOOLEAN = 'BOOLEAN', _('Boolean Value')
        PHONE_NUMBER = 'PHONE_NUMBER', _('Phone Number')
        LIST = 'LIST', _('List')

    name = models.CharField(max_length=255)
    description = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    field_type = models.CharField(max_length=20, choices=FieldType.choices, default=FieldType.TEXT_FIELD)
    validation_type = models.CharField(choices=ValidationType.choices, max_length=20, default=ValidationType.NONE)
    validation_value = models.CharField(max_length=255, blank=True, default='')
    default_value = models.CharField(max_length=255, null=True, blank=True)
    is_required = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} | {self.content_object}'
