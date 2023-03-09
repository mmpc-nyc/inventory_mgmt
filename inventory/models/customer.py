from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from phonenumber_field.modelfields import PhoneNumberField
from common.models.location import Location
from common.models.contact import Contact


class Customer(MPTTModel):
    class CustomerType(models.TextChoices):
        RESIDENTIAL = 'Residential', _('Residential')
        COMMERCIAL = 'Commercial', _('Commercial')

    customer_type = models.CharField(verbose_name=_('Type'), max_length=32, choices=CustomerType.choices)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    company_name = models.CharField(max_length=150, blank=True, default='')
    email = models.EmailField(blank=True)
    phone_number = PhoneNumberField(default='', blank=True)
    contacts = models.ManyToManyField(Contact, through='CustomerContact', verbose_name=_('Customer Contacts'), related_name='customer_contacts')
    billing_location = models.ForeignKey(Location, verbose_name=_('Billing Location'),
                                         related_name='billing_location', on_delete=models.CASCADE)
    service_locations = models.ManyToManyField(Location, through='ServiceLocation', related_name='service_locations')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    def get_absolute_url(self):
        return reverse_lazy('inventory:customer_detail', kwargs={'pk': self.pk})

    @property
    def name(self) -> str:
        return f'{self.company_name}' if self.company_name else f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class MPTTMeta:
        order_insertion_by = ['company_name', 'first_name', 'last_name', ]

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')
        ordering = ('company_name', 'first_name', 'last_name',)


class ServiceLocation(models.Model):
    """Service Locations for Customer."""
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.location} | {self.customer}'

    class Meta:
        verbose_name = _('Service Location')
        verbose_name_plural = _('Service Locations')


class CustomerContact(models.Model):
    """Contacts associated with the customer"""
    customer = models.ForeignKey('Customer', verbose_name=_('Customer'), on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, verbose_name=_('Contact'), on_delete=models.CASCADE)
