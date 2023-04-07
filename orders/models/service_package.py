from django.db import models
from django.utils.translation import gettext_lazy as _


class ServicePackage(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Service Package')
        verbose_name_plural = _('Service Packages')


class ServicePackageItem(models.Model):
    service = models.ForeignKey('orders.Service', on_delete=models.CASCADE)
    service_package = models.ForeignKey('ServicePackage', on_delete=models.CASCADE)
    sequence = models.PositiveSmallIntegerField(default=1)
    is_follow_up = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    days_after_previous_service = models.PositiveSmallIntegerField(default=0, blank=True)
    days_before_next_service = models.PositiveSmallIntegerField(default=0, blank=True)
    interval = models.CharField(max_length=16, blank=True)

    def __str__(self):
        return f'{self.service.name} - {self.service_package.name}'

    class Meta:
        verbose_name = _('Service Package Item')