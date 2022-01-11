from collections import defaultdict

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse_lazy
from django.utils.functional import cached_property
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from phonenumber_field.modelfields import PhoneNumberField
from simple_history.models import HistoricalRecords

from inventory.exceptions import OrderCompletionError


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


class Location(models.Model):
    name = models.CharField(max_length=150, blank=True)
    street_number = models.CharField(max_length=20, blank=True)
    route = models.CharField(max_length=100, blank=True)
    raw = models.CharField(max_length=200)
    formatted = models.CharField(max_length=200, blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    history = HistoricalRecords()

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


class Customer(MPTTModel):
    #  TODO  Write Description
    #  TODO  Fix bug with history model
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    company_name = models.CharField(max_length=150, blank=True, default='')
    contacts = models.ManyToManyField('Contact', through='CustomerContact', related_name='contact')
    locations = models.ManyToManyField('Location', through='CustomerLocation', related_name='location')
    parent = TreeForeignKey('self', on_delete=models.PROTECT, blank=True, null=True)

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


class CustomerLocation(models.Model):
    #  TODO  Write Description
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.location} | {self.customer}'

    class Meta:
        verbose_name = _('Customer Location')
        verbose_name_plural = _('Customer Locations')


class CustomerContact(models.Model):
    #  TODO  Write Description
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    contact = models.ForeignKey('Contact', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.customer} | {self.contact}'

    class Meta:
        verbose_name = _('Customer Contact')
        verbose_name_plural = _('Customer Contacts')


User = get_user_model()


class Equipment(models.Model):
    """A product that is can be stored, deployed, and picked up. """

    class Status(models.TextChoices):
        """Current status of the product"""

        STORED = 'STORED', _('Stored')  # Equipment stored in Stock
        DEPLOYED = 'DEPLOYED', _('Deployed')  # Equipment is currently deployed at order location
        PICKED_UP = 'PICKED_UP', _('Picked Up')  # Equipment is with the employee
        MISSING = 'MISSING', _('Missing')  # Equipment cannot be found.

    name = models.CharField(max_length=150, blank=True, null=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    status = models.CharField(max_length=32, choices=Status.choices, default=Status.STORED)
    stock = models.ForeignKey('Stock', on_delete=models.SET_NULL, blank=True, null=True)
    condition = models.ForeignKey('Condition', on_delete=models.PROTECT)
    user = models.ForeignKey(User, related_name='equipment_employee', on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True)
    counter = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Equipment')
        verbose_name_plural = _('Equipment')

    def get_absolute_url(self):
        return reverse_lazy('inventory:equipment_detail', kwargs={'pk': self.pk})

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # TODO  Review This Method for uniqueness and usefulness
        if not self.name:
            self.name = self.name or slugify(
                f'{self.product.generic_product.name} {self.product.id} {self.product.counter}')
            self.counter = self.product.counter
            self.product.counter += 1
            self.product.save()
        return super().save(force_insert, force_update, using, update_fields)


class Condition(models.Model):
    """Physical condition of the product that determines if it can be used"""
    name = models.CharField(verbose_name=_('name'), max_length=32)
    description = models.TextField(verbose_name=_('description'))
    actions = models.ManyToManyField('EquipmentTransactionAction')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Condition')
        verbose_name_plural = _('Conditions')


class GenericProduct(models.Model):
    """A generic product container that relates to different versions of the same product.
    For example: a product having different brands or different sizes or colors
    """

    class Status(models.TextChoices):
        """Product status choices
        Stored: Product stored in Stock
        Deployed: Product deployed at customer location
        Decommissioned: Product no longer in use and not in inventory
        Inactive: The product is no longer active but is still stored in the inventory
        Recall: The product is inactive and should no longer be used.
        Picked Up: Product is currently with the user. Not at any customer location or inventory.
        """
        ACTIVE = 'Active', _('Active')
        INACTIVE = 'Inactive', _('Inactive')
        RECALL = 'Recall', _('Recall')

    category = TreeForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=150, unique=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.ACTIVE)
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Generic Product')
        verbose_name_plural = _('Generic Products')


class Category(MPTTModel):
    name = models.CharField(max_length=64)
    slug = models.SlugField()
    parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    class MPTTMeta:
        order_insertion_by = ['name', ]

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    """TODO  Write Description"""

    class Status(models.TextChoices):
        """Product status choices
        TODO  Rethink this
        """
        ACTIVE = 'Active', _('Active')  # Can be used and allows purchasing of new equipment
        INACTIVE = 'Inactive', _('Inactive')  # The product is no longer active but is still stored in the inventory
        RECALL = 'Recall', _('Recall')  # The product is inactive and should no longer be used.

    name = models.CharField(max_length=150)
    generic_product = models.ForeignKey('GenericProduct', on_delete=models.PROTECT)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    product_type = models.ForeignKey('ProductType', on_delete=models.CASCADE)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.ACTIVE)
    counter = models.IntegerField(default=0)

    @cached_property
    def count(self):
        return self.equipment_set.count()

    @cached_property
    def stored_count(self):
        return self.equipment_set.filter(status=Equipment.Status.STORED).quantity()

    @cached_property
    def deployed_count(self):
        return self.equipment_set.filter(status=Equipment.Status.DEPLOYED).quantity()

    @cached_property
    def picked_up_count(self):
        return self.equipment_set.filter(status=Equipment.Status.PICKED_UP).quantity()

    def __str__(self):
        return f'{self.name} | {self.brand.name}'

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def get_absolute_url(self):
        return reverse_lazy('inventory:product_detail', kwargs={'pk': self.pk})


class ProductType(models.Model):
    #  TODO  Write Description
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Product Type')
        verbose_name_plural = _('Product Types')


class Brand(models.Model):
    #  TODO  Write Description
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')


class Stock(models.Model):
    """A holder for all equipment"""

    class StockStatus(models.TextChoices):
        """Choices for setting the status of a stock location
        Active: Available for picking up and dropping off items
        Inactive: Not in use. Products cannot be picked up or dropped off from this location
        Full: The inventory location is currently full. No items can be dropped off.
        """

        ACTIVE = 'Active', _('Active')
        INACTIVE = 'Inactive', _('Inactive')
        FULL = 'Full', _('Full')

    name = models.CharField(max_length=150, blank=True)
    status = models.CharField(max_length=32, choices=StockStatus.choices, default=StockStatus.ACTIVE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Stock')
        verbose_name_plural = _('Stocks')

    def get_absolute_url(self):
        return reverse_lazy('stock:stock_detail', kwargs={'pk': self.pk})


class EquipmentTransaction(models.Model):
    class TransactionType(models.TextChoices):
        STORE = 'Store', _('Store')
        PICK_UP = 'Pick_Up', _('Pick Up')
        DEPLOY = _('Deploy')
        TRANSFER = _('Transfer')
        WITHDRAW = _('Withdraw')
        DECOMMISSION = _('Decommission')

    equipment = models.ForeignKey(Equipment, verbose_name=_('equipment'), on_delete=models.PROTECT)
    action = models.CharField(verbose_name=_('type'), max_length=32, choices=TransactionType.choices)
    user = models.ForeignKey(get_user_model(), verbose_name=_('user'), on_delete=models.PROTECT)
    condition = models.ForeignKey(Condition, verbose_name=_('condition'), on_delete=models.PROTECT)
    timestamp = models.DateTimeField(verbose_name=_('timestamp'), auto_now=True)

    def __str__(self):
        return f'{self.action} {self.equipment} at {self.timestamp} by {self.user}'

    class Meta:
        verbose_name = _('Equipment Transaction')
        verbose_name_plural = _('Equipment Transactions')


class EquipmentTransactionAction(models.Model):
    name = models.CharField(verbose_name=_('name'), max_length=32, unique=True)
    description = models.TextField(verbose_name=_('description'))


class Order(models.Model):
    """Model for scheduling orders to allow easier assignment of inventory, services and products"""

    class Activity(models.TextChoices):
        DEPLOY = 'Deploy', _('Deploy')
        PICKUP = 'Pickup', _('Pickup')
        INSPECT = 'Inspect', _('Inspect')

    class Status(models.TextChoices):
        NEW = 'New', _('New')
        ASSIGNED = 'Assigned', _('Assigned')
        IN_PROGRESS = 'In Progress', _('In Progress')
        COMPLETED = 'Completed', _('Completed')
        CANCELED = 'Canceled', _('Canceled')

    customer = models.ForeignKey(Customer, verbose_name=_('customer'), on_delete=models.CASCADE)
    activity = models.CharField(verbose_name=_('activity'), max_length=32, choices=Activity.choices,
                                default=Activity.DEPLOY)
    status = models.CharField(max_length=16, verbose_name=_('status'), choices=Status.choices, default=Status.NEW)
    users = models.ManyToManyField(get_user_model(), verbose_name=_('users'), related_name='order_users')
    location = models.ForeignKey(Location, verbose_name=_('location'), on_delete=models.CASCADE)
    date = models.DateTimeField()
    equipments = models.ManyToManyField('Equipment', verbose_name=_('equipments'), through='OrderEquipment',
                                        related_name='equipments')
    generic_products = models.ManyToManyField('GenericProduct', verbose_name=_('generic products'),
                                              through='OrderGenericProduct', related_name='generic_products')
    history = HistoricalRecords()

    def get_deployed_equipment(self):
        return self.equipments.filter(status=Equipment.Status.DEPLOYED)

    def missing_equipment_validator(self, ignore_issues: True):
        """If there is any equipment that is still deployed the completion will fail unless the
        "ignore_issues" is true then the status of the remaining deployed equipment will
        be set to MISSING"""

        deployed_equipment = self.get_deployed_equipment()
        if deployed_equipment:
            if not ignore_issues:
                raise OrderCompletionError('Not all equipment has been picked up')
            deployed_equipment.update(status=Equipment.Status.MISSING)

    def complete(self, ignore_issues: bool = False):
        """Completes the order"""
        if self.status in {self.Status.COMPLETED, self.Status.CANCELED}:
            raise OrderCompletionError(f'Cannot complete order with status of {self.status}')
        if self.activity == self.Activity.DEPLOY:
            self._complete_deploy_activity(ignore_issues=ignore_issues)
        elif self.activity == self.Activity.PICKUP:
            self._complete_pickup_activity(ignore_issues=ignore_issues)
        elif self.activity == self.Activity.INSPECT:
            self._complete_inspection_activity(ignore_issues=ignore_issues)
        self.status = self.Status.COMPLETED
        self.save()

    def _complete_deploy_activity(self, ignore_issues: bool):
        if self.activity != self.Activity.DEPLOY:
            return
        if ignore_issues:
            return

        generic_product_dict = defaultdict(int)
        for order_generic_product in self.ordergenericproduct_set.all():
            generic_product_dict[order_generic_product.pk] = order_generic_product.quantity
        for order_equipment in self.orderequipment_set.all():
            related_id = order_equipment.equipment.product.generic_product.id
            if related_id not in generic_product_dict:
                raise OrderCompletionError(
                    'Equipment that is not part of the order cannot be deployed unless ignore checks is enabled')
            generic_product_dict[related_id] -= 1
        for generic_product_id, quantity in generic_product_dict.items():
            if quantity != 0:
                raise OrderCompletionError(
                    'A quantity mismatch was found between requested equipment and deployed equipment. '
                    'To bypass this error ignore checks should be enabled')

    def _complete_pickup_activity(self, ignore_issues: bool):
        self.missing_equipment_validator(ignore_issues)

    def _complete_inspection_activity(self, ignore_issues: bool):
        ...

    def cancel(self, ignore_issues: bool = False):
        """Cancels the order"""
        self.missing_equipment_validator(ignore_issues=ignore_issues)
        self.status = self.Status.CANCELED
        self.save()

    def save(self, **kwargs):
        # TODO Implement a method that only allows updates if the order is in active status.
        if self.status:
            ...
        return super().save(**kwargs)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return f'{self.id}'


class OrderGenericProduct(models.Model):
    """A link table for managing the required/recommended generic products needed to fill an order"""

    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    generic_product = models.ForeignKey('GenericProduct', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.order} | {self.generic_product} | {self.quantity}'

    class Meta:
        verbose_name = _('Order Generic Product')
        verbose_name_plural = _('Order Generic Product')
        unique_together = ('order', 'generic_product')


class OrderEquipment(models.Model):
    """A link table for mapping the equipment associated with the order"""

    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    equipment = models.ForeignKey('Equipment', on_delete=models.CASCADE)
    deployed = models.DateTimeField()
    picked_up = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.order} | {self.equipment}'

    class Meta:
        verbose_name = _('Order Equipment')
        verbose_name_plural = _('Order Equipment')
        unique_together = ('order', 'equipment')
