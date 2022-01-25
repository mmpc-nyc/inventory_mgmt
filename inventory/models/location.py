from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class Location(models.Model):
    name = models.CharField(max_length=150, blank=True)
    street_number = models.CharField(max_length=20, blank=True)
    route = models.CharField(max_length=100, blank=True)
    raw = models.CharField(max_length=200)
    formatted = models.CharField(max_length=200, blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse_lazy('inventory:location_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        self.name = self.name or self.formatted or self.raw
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')
        ordering = ('name',)


class LocationContact(models.Model):
    """Contacts associated with specific locations"""
    location = models.ForeignKey('Location', verbose_name=_('Location'), on_delete=models.CASCADE)
    contact = models.ForeignKey('Contact', verbose_name=_('Contact'), on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.location} | {self.contact}'

    class Meta:
        verbose_name = _('Location Contact')
        verbose_name_plural = _('Location Contacts')
