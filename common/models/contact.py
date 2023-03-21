from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class Contact(models.Model):
    """Model for managing contacts that attach to customers and employees"""
    PREFERRED_CONTACT_CHOICES = [
        ('PHONE', 'Phone'),
        ('EMAIL', 'Email'),
    ]

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    preferred_contact_method = models.CharField(max_length=10, choices=PREFERRED_CONTACT_CHOICES, default='PHONE')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')
        ordering = ('first_name', 'last_name',)


class ContactPhoneNumber(models.Model):
    """
    Model for managing phone numbers associated with a contact.
    """
    contact = models.ForeignKey('Contact', on_delete=models.CASCADE)
    phone_number = PhoneNumberField(default='', blank=True)
    phone_type = models.ForeignKey('PhoneNumberType', on_delete=models.SET_NULL, null=True, blank=True)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.contact} | {self.phone_number}'

    class Meta:
        verbose_name = _('Contact Phone Number')
        verbose_name_plural = _('Contact Phone Numbers')



    def save(self, *args, **kwargs):
        if self.is_primary:
            # Set all other phone numbers for this contact as not primary
            self.contact.contactphonenumber_set.exclude(pk=self.pk).update(is_primary=False)

        super().save(*args, **kwargs)


class ContactEmail(models.Model):
    """
    Model for managing email addresses associated with a contact.
    """
    contact = models.ForeignKey('Contact', on_delete=models.CASCADE)
    email = models.EmailField(blank=True)
    email_type = models.ForeignKey('EmailType', on_delete=models.SET_NULL, null=True, blank=True)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = _('Contact Email')
        verbose_name_plural = _('Contact Emails')

    def save(self, *args, **kwargs):
        if self.is_primary:
            # Set all other emails for this contact as not primary
            self.contact.contactemail_set.exclude(pk=self.pk).update(is_primary=False)

        super().save(*args, **kwargs)


class PhoneNumberType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class EmailType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
