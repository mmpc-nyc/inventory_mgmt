from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from phonenumber_field.modelfields import PhoneNumberField

from common.models.address import Address
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
    contacts = models.ManyToManyField(Contact, through='customers.CustomerContact', verbose_name=_('Customer Contacts'),
                                      related_name='customer_contacts')
    service_locations = models.ManyToManyField('customers.ServiceLocation', related_name='service_locations')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    def get_absolute_url(self):
        return reverse_lazy('inventory:customer_detail', kwargs={'pk': self.pk})

    @property
    def name(self) -> str:
        return f'{self.company_name}' if self.company_name else f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.pk} {self.name}'

    @property
    def primary_service_location(self):
        try:
            return self.service_locations.get(is_primary=True)
        except ServiceLocation.DoesNotExist:
            return None

    class MPTTMeta:
        order_insertion_by = ['company_name', 'first_name', 'last_name', ]

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')
        ordering = ('company_name', 'first_name', 'last_name', 'pk',)


class ServiceLocation(Address):
    """
    Model for a service location associated with a customer.
    A customer can have multiple service locations.
    """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_service_locations')
    contacts = models.ManyToManyField('common.Contact', related_name='service_location_contacts')
    is_active = models.BooleanField(default=True)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Service Location')
        verbose_name_plural = _('Service Locations')


class BillingLocation(Address):
    """
    Model for a billing location associated with a customer.
    A customer can only have one billing location.
    """
    customer = models.OneToOneField('customers.Customer', on_delete=models.CASCADE)
    contacts = models.ManyToManyField('common.Contact', related_name='billing_location_contacts')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Billing Location')
        verbose_name_plural = _('Billing Locations')


class CustomerContact(models.Model):
    """Contacts associated with the customer"""
    customer = models.ForeignKey('Customer', verbose_name=_('Customer'), on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, verbose_name=_('Contact'), on_delete=models.CASCADE)
