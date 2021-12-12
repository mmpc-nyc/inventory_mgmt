from django.db import models
from django.urls import reverse_lazy
from phonenumber_field.modelfields import PhoneNumberField

from .helper_models import CreatedUpdatedModel


class Customer(CreatedUpdatedModel):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    company_name = models.CharField(max_length=150, blank=True, default='')
    email = models.EmailField(blank=True)
    location = models.ManyToManyField('Location', through='CustomerLocation', related_name='location')

    def get_absolute_url(self):
        return reverse_lazy('main:customer_detail', kwargs={'pk': self.pk})

    @property
    def name(self) -> str:
        return f'{self.company_name}' if self.company_name else f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ('company_name', 'first_name', 'last_name',)


class Contact(CreatedUpdatedModel):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    phone_number = PhoneNumberField(default='', blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ('first_name', 'last_name', 'email',)


