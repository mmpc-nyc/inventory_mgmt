from django.contrib.auth import get_user_model
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from simple_history.models import HistoricalRecords
from inventory.exceptions import ProductStatusError, StockLogicError, ProductConditionError


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


class Contact(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    phone_number = PhoneNumberField(default='', blank=True)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')
        ordering = ('first_name', 'last_name', 'email',)


class Customer(MPTTModel):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    company_name = models.CharField(max_length=150, blank=True, default='')
    email = models.EmailField(blank=True)
    location = models.ManyToManyField('Location', through='CustomerLocation', related_name='location')
    history = HistoricalRecords()
    parent = TreeForeignKey('self', on_delete=models.PROTECT)

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


class ProductStatus(models.TextChoices):
    """Product status choices
    Stored: Product stored in Inventory
    Deployed: Product deployed at customer location
    Decommissioned: Product no longer in use and not in inventory
    Inactive: The product is no longer active but is still stored in the inventory
    Recall: The product is inactive and should no longer be used.
    Picked Up: Product is currently with the employee. Not at any customer location or inventory.
    """
    STORED = 'STORED', _('Stored')
    DEPLOYED = 'DEPLOYED', _('Deployed')
    DECOMMISSIONED = 'DECOMMISSIONED', _('Decommissioned')
    INACTIVE = 'INACTIVE', _('Inactive')
    RECALL = 'RECALL', _('Recall')
    PICKED_UP = 'PICKED_UP', _('Picked Up')


class GenericProduct(models.Model):
    """A generic product container that relates to different versions of the same product.
    For example: a product having different brands or different sizes or colors
    """
    category = TreeForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=150, unique=True)
    status = models.CharField(max_length=16, choices=ProductStatus.choices, default=ProductStatus.STORED)
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Generic Product')
        verbose_name_plural = _('Generic Products')


class Brand(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')


class ProductType(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Product Type')
        verbose_name_plural = _('Product Types')


class Product(models.Model):
    """An inventory item that can be inventoried"""

    class Condition(models.TextChoices):
        """Current condition of an inventory item. New: Brand new inventory item that has not been used. When the
        inventory item is picked up it is automatically changed to working. Working: Product is in good working
        condition Damaged: Product is damaged and needs repair Irreparable: Product is damaged beyond repair. This
        inventory item should be decommissioned
        """
        NEW = 'NEW', _('New')
        WORKING = 'WORKING', _('Working')
        DAMAGED = 'DAMAGED', _('Damaged')
        IRREPARABLE = 'IRREPARABLE', _('Irreparable')

    name = models.ForeignKey('GenericProduct', on_delete=models.PROTECT)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    status = models.CharField(max_length=16, choices=ProductStatus.choices, default=ProductStatus.STORED)
    condition = models.CharField(max_length=16, choices=Condition.choices, default=Condition.NEW)
    inventory = models.ForeignKey('Stock', on_delete=models.SET_NULL, blank=True, null=True)
    employee = models.ForeignKey(get_user_model(), related_name='product_employee', on_delete=models.SET_NULL,
                                 null=True, blank=True)
    job = models.ForeignKey('Job', on_delete=models.SET_NULL, null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def get_absolute_url(self):
        return reverse_lazy('inventory:product_detail', kwargs={'pk': self.pk})

    def store(self, inventory_id: int = None) -> 'Product':
        """Stores the inventory item at a inventory location. By default the inventory item is returned to it's
        original location. If a inventory_id is supplied the inventory item is moved to a new inventory location with
        the given inventory_id """
        if self.status == ProductStatus.DECOMMISSIONED:
            raise ProductStatusError('decommissioned inventory item cannot be stored')
        if inventory_id is None and self.inventory_id is None:
            raise StockLogicError(
                _('the current inventory item does not have a inventory associated with it. A inventory_id must be '
                  'passed'))
        if self.status == ProductStatus.STORED and self.inventory_id and inventory_id and int(self.inventory_id) == int(
                inventory_id):
            raise StockLogicError(_('cannot store inventory item in a location it is already stored in'))
        if inventory_id is not None:
            self.inventory_id = inventory_id
        self.location_id = Stock.objects.get(id=inventory_id).location_id
        self.employee = None
        self.status = ProductStatus.STORED
        return self.save()

    def pickup(self, employee_id: int) -> 'Product':
        """Product is picked up from a customer location or a inventory location. An employee is assigned to the
        inventory item. """
        if self.status == ProductStatus.DECOMMISSIONED:
            raise ProductStatusError(_('decommissioned inventory item cannot be picked up'))
        if self.condition == self.Condition.NEW:
            self.condition = self.Condition.WORKING
        if self.employee_id == employee_id:
            raise StockLogicError(_('the same user cannot pick up an inventory item they are already holding'))
        self.location = None
        self.employee_id = employee_id
        self.status = ProductStatus.PICKED_UP
        return self.save()

    def deploy(self, location_id: int) -> 'Product':
        """Deploys the inventory item at a customer location"""
        if self.status == ProductStatus.DECOMMISSIONED:
            raise ProductStatusError(_('decommissioned inventory item cannot be deployed'))
        if self.status != ProductStatus.PICKED_UP:
            raise ProductStatusError(_('item must be picked up before it can be deployed'))
        if self.condition in self.Condition.DAMAGED or self.Condition.IRREPARABLE:
            raise ProductConditionError(_('broken or irreparable item cannot be deployed'))
        self.location_id = location_id
        self.status = ProductStatus.DEPLOYED
        return self.save()

    def decommission(self) -> 'Product':
        """Decommissions the item and removes all employee, inventory, and location associations"""
        notification_message: str = ''  # TODO  Add notification message for decommissioning an item.
        self.location = None
        self.employee = None
        self.inventory = None
        self.status = ProductStatus.DECOMMISSIONED
        return self.save()

    def save(self, *args, **kwargs):
        if self.inventory and not self.location:
            self.location_id = self.inventory.location_id
        return super().save(*args, **kwargs)


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
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)


class Stock(models.Model):
    """A holder for all inventory items"""

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


class Job(models.Model):
    """Model for scheduling jobs to allow easier assignment of inventory, services and products"""

    class JobStatus(models.TextChoices):
        ACTIVE = 'ACTIVE', _('Active')
        CANCELED = 'CANCELED', _('Canceled')
        COMPLETED = 'COMPLETED', _('Completed')

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(max_length=16, choices=JobStatus.choices, default=JobStatus.ACTIVE)
    employee = models.ManyToManyField(get_user_model(), related_name='job_employees')
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    date = models.DateTimeField()
    history = HistoricalRecords()

    def save(self, **kwargs):
        # TODO Implement a method that only allows updates if the job is in active status.
        print(kwargs)
        # if self.status == self.JobStatus.ACTIVE:
        return super().save(**kwargs)

    class Meta:
        verbose_name = _('Job')
        verbose_name_plural = _('Jobs')

    def __str__(self):
        return f'Job {self.id} for {self.customer} @ {self.date}'
