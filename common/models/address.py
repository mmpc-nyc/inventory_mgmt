from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class Address(models.Model):
    name = models.CharField(max_length=150, blank=True)
    address_line_1 = models.CharField(max_length=150)
    address_line_2 = models.CharField(max_length=150, blank=True)
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
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')
        ordering = ('name',)