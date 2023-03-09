from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from common.models.contact import Contact


class Location(models.Model):
    name = models.CharField(max_length=150, blank=True)
    address_line_1 = models.TextField()
    address_line_2 = models.TextField(default="", blank=True, null=True)
    city = models.CharField(max_length=32)
    state = models.CharField(max_length=32)
    postal_code = models.CharField(max_length=5)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse_lazy('inventory:location_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')
        ordering = ('name',)


class LocationContact(models.Model):
    """Contacts associated with specific locations"""
    location = models.ForeignKey('Location', verbose_name=_('Location'), on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, verbose_name=_('Contact'), on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.location} | {self.contact}'

    class Meta:
        verbose_name = _('Location Contact')
        verbose_name_plural = _('Location Contacts')
