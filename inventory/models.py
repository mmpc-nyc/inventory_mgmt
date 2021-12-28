from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from simple_history.models import HistoricalRecords
from inventory.exceptions import ProductStatusError, StockLogicError, ProductConditionError, ProductOrderAssignmentError


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


class ContactEmail(models.Model):
    #  TODO  Write Description
    contact = models.ForeignKey('Contact', on_delete=models.CASCADE)
    email = models.ForeignKey('Email', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class ContactPhoneNumber(models.Model):
    #  TODO  Write Description
    contact = models.ForeignKey('Contact', on_delete=models.CASCADE)
    phone_number = models.ForeignKey('PhoneNumber', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.contact} | {self.phone_number}'

    class Meta:
        verbose_name = _('Contact Phone Number')
        verbose_name_plural = _('Contact Phone Numbers')


class CustomerContact(models.Model):
    #  TODO  Write Description
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    contact = models.ForeignKey('Contact', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.customer} | {self.contact}'

    class Meta:
        verbose_name = _('Customer Contact')
        verbose_name_plural = _('Customer Contacts')


class Customer(MPTTModel):
    #  TODO  Write Description
    #  TODO  Fix bug with history model
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    company_name = models.CharField(max_length=150, blank=True, default='')
    contact = models.ManyToManyField('Contact', through='CustomerContact', related_name='contact')
    location = models.ManyToManyField('Location', through='CustomerLocation', related_name='location')
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
        Picked Up: Product is currently with the employee. Not at any customer location or inventory.
        """
        ACTIVE = 'ACTIVE', _('Active')
        INACTIVE = 'INACTIVE', _('Inactive')
        RECALL = 'RECALL', _('Recall')

    category = TreeForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=150, unique=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.ACTIVE)
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Generic Product')
        verbose_name_plural = _('Generic Products')


class Brand(models.Model):
    #  TODO  Write Description
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')


class ProductType(models.Model):
    #  TODO  Write Description
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Product Type')
        verbose_name_plural = _('Product Types')


class Product(models.Model):
    """TODO  Write Description"""

    class Status(models.TextChoices):
        """Product status choices
        Active: Can be used and allows purchasing of new equipment
        Inactive: The product is no longer active but is still stored in the inventory
        Recall: The product is inactive and should no longer be used.
        """
        ACTIVE = 'ACTIVE', _('Active')
        INACTIVE = 'INACTIVE', _('Inactive')
        RECALL = 'RECALL', _('Recall')

    name = models.CharField(max_length=150)
    generic_name = models.ForeignKey('GenericProduct', on_delete=models.PROTECT)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.ACTIVE)
    counter = models.IntegerField(default=0)

    @property
    def count(self):
        return self.equipment_set.count()

    @property
    def stored_count(self):
        return self.equipment_set.filter(status=Equipment.Status.STORED).count()

    @property
    def deployed_count(self):
        return self.equipment_set.filter(status=Equipment.Status.DEPLOYED).count()

    @property
    def decommissioned_count(self):
        return self.equipment_set.filter(status=Equipment.Status.DECOMMISSIONED).count()

    @property
    def picked_up_count(self):
        return self.equipment_set.filter(status=Equipment.Status.PICKED_UP).count()

    def __str__(self):
        return f'{self.name} | {self.brand.name}'

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def get_absolute_url(self):
        return reverse_lazy('inventory:product_detail', kwargs={'pk': self.pk})


class Equipment(models.Model):
    # TODO  Write Description

    class Condition(models.TextChoices):
        """Current condition of an equipment. New: Brand new equipment that has not been used. When the
        equipment is picked up it is automatically changed to working. Working: Product is in good working
        condition Damaged: Product is damaged and needs repair Irreparable: Product is damaged beyond repair. This
        equipment should be decommissioned
        """
        NEW = 'NEW', _('New')
        WORKING = 'WORKING', _('Working')
        DAMAGED = 'DAMAGED', _('Damaged')
        IRREPARABLE = 'IRREPARABLE', _('Irreparable')

    class Status(models.TextChoices):
        """Product status choices
        Stored: Product stored in Stock
        Deployed: Product deployed at customer location
        Decommissioned: Product no longer in use and not in inventory
        Inactive: The product is no longer active but is still stored in the inventory
        Recall: The product is inactive and should no longer be used.
        Picked Up: Product is currently with the employee. Not at any customer location or inventory.
        """
        STORED = 'STORED', _('Stored')
        DEPLOYED = 'DEPLOYED', _('Deployed')
        DECOMMISSIONED = 'DECOMMISSIONED', _('Decommissioned')
        PICKED_UP = 'PICKED_UP', _('Picked Up')

    name = models.CharField(max_length=150, blank=True, null=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.STORED)
    condition = models.CharField(max_length=16, choices=Condition.choices, default=Condition.NEW)
    stock = models.ForeignKey('Stock', on_delete=models.SET_NULL, blank=True, null=True)
    employee = models.ForeignKey(get_user_model(), related_name='product_employee', on_delete=models.SET_NULL,
                                 null=True, blank=True)
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True, blank=True)
    counter = models.IntegerField(blank=True, null=True)
    history = HistoricalRecords()

    def store(self, stock_id: int = None) -> 'Equipment':
        """Stores the equipment at a stock location. By default the equipment is returned to it's
        original location. If a stock_id is supplied the equipment is moved to a new equipment location with
        the given stock_id """
        if self.status == self.Status.DECOMMISSIONED:
            raise ProductStatusError('decommissioned equipment cannot be stored')
        if stock_id is None and self.stock_id is None:
            raise StockLogicError(
                _('the current equipment does not have a inventory associated with it. A inventory_id must be '
                  'passed'))
        if self.status == self.Status.STORED and self.stock_id and stock_id and int(self.stock_id) == int(stock_id):
            raise StockLogicError(_('cannot store stock item in a location it is already stored in'))
        if stock_id is not None:
            self.stock_id = stock_id
        self.employee = None
        self.status = self.Status.STORED
        return self.save()

    def pickup(self, employee_id: int) -> 'Equipment':
        """Product is picked up from a customer location or a inventory location. An employee is assigned to the
        equipment. """
        if self.status == self.Status.DECOMMISSIONED:
            raise ProductStatusError(_('decommissioned equipment cannot be picked up'))
        if self.condition == self.Condition.NEW:
            self.condition = self.Condition.WORKING
        if self.employee_id == employee_id:
            raise StockLogicError(_('the same user cannot pick up an equipment they are already holding'))
        self.employee_id = employee_id
        self.status = self.Status.PICKED_UP
        return self.save()

    def deploy(self, order_id: int = None) -> 'Equipment':
        if not order_id and not self.order:
            raise ProductOrderAssignmentError(_('A order must be assigned to deploy the product'))
        self.order = order_id or self.order
        """Deploys the equipment at a customer location"""
        if self.status == self.Status.DECOMMISSIONED:
            raise ProductStatusError(_('decommissioned equipment cannot be deployed'))
        if self.status != self.Status.PICKED_UP:
            raise ProductStatusError(_('item must be picked up before it can be deployed'))
        if self.condition in self.Condition.DAMAGED or self.Condition.IRREPARABLE:
            raise ProductConditionError(_('broken or irreparable item cannot be deployed'))
        self.status = self.Status.DEPLOYED
        return self.save()

    def decommission(self) -> 'Equipment':
        """Decommissions the item and removes all employee, inventory, and location associations"""
        notification_message: str = ''  # TODO  Add notification message for decommissioning an item.
        self.employee = None
        self.stock = None
        self.status = self.Status.DECOMMISSIONED
        return self.save()

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
            self.name = slugify(f'{self.product.generic_name.name} {self.product.id} {self.product.counter}')
            self.counter = self.product.counter
            self.product.counter += 1
            self.product.save()
        return super().save(force_insert, force_update, using, update_fields)


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


class CustomerLocation(models.Model):
    #  TODO  Write Description
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.location} | {self.customer}'

    class Meta:
        verbose_name = _('Customer Location')
        verbose_name_plural = _('Customer Locations')


class Stock(models.Model):
    """A holder for all equipment"""

    class StockStatus(models.TextChoices):
        """Choices for setting the status of a stock location
        Active: Available for picking up and dropping off items
        Inactive: Not in use. Products cannot be picked up or dropped off from this location
        Full: The inventory location is currently full. No items can be dropped off.
        """

        ACTIVE = 'ACTIVE', _('Active')
        INACTIVE = 'INACTIVE', _('Inactive')
        FULL = 'FULL', _('Full')

    name = models.CharField(max_length=150, blank=True)
    status = models.CharField(max_length=16, choices=StockStatus.choices, default=StockStatus.ACTIVE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Stock')
        verbose_name_plural = _('Stocks')

    def get_absolute_url(self):
        return reverse_lazy('stock:stock_detail', kwargs={'pk': self.pk})


class Notification(models.Model):
    """TODO  Implement this class"""
    pass


class NotificationPreference(models.Model):
    """TODO  Implement this class"""
    pass


class Order(models.Model):
    """Model for scheduling orders to allow easier assignment of inventory, services and products"""

    class OrderStatus(models.TextChoices):
        ACTIVE = 'ACTIVE', _('Active')
        CANCELED = 'CANCELED', _('Canceled')
        COMPLETED = 'COMPLETED', _('Completed')

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(max_length=16, choices=OrderStatus.choices, default=OrderStatus.ACTIVE)
    employee = models.ManyToManyField(get_user_model(), related_name='order_employees')
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    date = models.DateTimeField()
    history = HistoricalRecords()

    def save(self, **kwargs):
        # TODO Implement a method that only allows updates if the order is in active status.
        return super().save(**kwargs)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return f'Order {self.id} for {self.customer} @ {self.date}'
