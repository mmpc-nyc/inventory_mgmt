from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from simple_history.models import HistoricalRecords


class Contact(models.Model):
    #  TODO  Write Description
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    emails = models.ManyToManyField('Email', through='ContactEmail', related_name='emails')
    phone_numbers = models.ManyToManyField('PhoneNumber', through='ContactPhoneNumber', related_name='phone_numbers')
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')
        ordering = ('first_name', 'last_name',)


class ContactPhoneNumber(models.Model):
    #  TODO  Write Description
    contact = models.ForeignKey('Contact', on_delete=models.CASCADE)
    phone_number = models.ForeignKey('PhoneNumber', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.contact} | {self.phone_number}'

    class Meta:
        verbose_name = _('Contact Phone Number')
        verbose_name_plural = _('Contact Phone Numbers')


class ContactEmail(models.Model):
    #  TODO  Write Description
    contact = models.ForeignKey('Contact', on_delete=models.CASCADE)
    email = models.ForeignKey('Email', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Email(models.Model):
    #  TODO  Write Description
    email = models.EmailField(blank=True)

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = _('Email')
        verbose_name_plural = _('Emails')


class PhoneNumber(models.Model):
    #  TODO  Write Description
    phone_number = PhoneNumberField(default='', blank=True)

    def __str__(self):
        return f'{self.phone_number}'

    class Meta:
        verbose_name = _('Phone Number')
        verbose_name_plural = _('Phone Numbers')