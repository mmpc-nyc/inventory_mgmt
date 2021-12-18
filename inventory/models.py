from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django_currentuser.db.models import CurrentUserField
from phonenumber_field.modelfields import PhoneNumberField
from simple_history.models import HistoricalRecords
from inventory.exceptions import ProductStatusError, InventoryLogicError, ProductConditionError


class CreatedUpdatedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Contact(CreatedUpdatedModel):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    phone_number = PhoneNumberField(default='', blank=True)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ('first_name', 'last_name', 'email',)


class Customer(CreatedUpdatedModel):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    company_name = models.CharField(max_length=150, blank=True, default='')
    email = models.EmailField(blank=True)
    location = models.ManyToManyField('Location', through='CustomerLocation', related_name='location')

    def get_absolute_url(self):
        return reverse_lazy('inventory:customer_detail', kwargs={'pk': self.pk})

    @property
    def name(self) -> str:
        return f'{self.company_name}' if self.company_name else f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ('company_name', 'first_name', 'last_name',)


class Product(CreatedUpdatedModel):
    """An inventory item that can be inventoried"""

    class ProductStatus(models.TextChoices):
        """Product status choices
        Stored: Product stored in Inventory
        Deployed: Product deployed at customer location
        Decommissioned: Product no longer in use and not in inventory
        Picked Up: Product is currently with the employee. Not at any customer location or inventory.
        """
        STORED = 'STORED', _('Stored')
        DEPLOYED = 'DEPLOYED', _('Deployed')
        DECOMMISSIONED = 'DECOMMISSIONED', _('Decommissioned')
        PICKED_UP = 'PICKED_UP', _('Picked Up')

    class Condition(models.TextChoices):
        """Current condition of an inventory item.
        New: Brand new inventory item that has not been used. When the inventory item is picked up it is automatically changed to working.
        Working: Product is in good working condition
        Damaged: Product is damaged and needs repair
        Irreparable: Product is damaged beyond repair. This inventory item should be decommissioned
        """
        NEW = 'NEW', _('New')
        WORKING = 'WORKING', _('Working')
        DAMAGED = 'DAMAGED', _('Damaged')
        IRREPARABLE = 'IRREPARABLE', _('Irreparable')

    class ProductNotificationMessage:
        """Possible class for selecting different kinds of inventory item based notification messages"""

    name = models.CharField(max_length=150)
    label = models.CharField(max_length=150, null=True, blank=True)
    job = models.ForeignKey('Job', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=16, choices=ProductStatus.choices, default=ProductStatus.STORED)
    employee = models.ForeignKey(get_user_model(), related_name='product_employee', on_delete=models.SET_NULL, null=True, blank=True)
    editor = CurrentUserField(related_name='product_editor', on_delete=models.SET_NULL, on_update=True)
    creator = CurrentUserField(related_name='product_creator', on_delete=models.SET_NULL)
    condition = models.CharField(max_length=16, choices=Condition.choices, default=Condition.NEW)
    inventory = models.ForeignKey('Inventory', on_delete=models.SET_NULL, blank=True, null=True)
    location = models.ForeignKey('Location', on_delete=models.SET_NULL, blank=True, null=True)
    product_type = models.ForeignKey('ProductType', on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse_lazy('inventory:product_detail', kwargs={'pk': self.pk})

    def store(self, inventory_id: int = None) -> 'Product':
        """Stores the inventory item at a inventory location. By default the inventory item is returned to it's original location.
        If a inventory_id is supplied the inventory item is moved to a new inventory location with the given inventory_id"""
        if self.status == self.ProductStatus.DECOMMISSIONED:
            raise ProductStatusError('decommissioned inventory item cannot be stored')
        if inventory_id is None and self.inventory_id is None:
            raise InventoryLogicError('the current inventory item does not have a inventory associated with it. A inventory_id must '
                                      'be passed')
        if self.status == Product.ProductStatus.STORED and type(self.inventory_id) != type(None) and type(inventory_id) != type(None) and int(self.inventory_id) == int(inventory_id):
            raise InventoryLogicError('cannot store inventory item in a location it is already stored in')
        if inventory_id is not None:
            self.inventory_id = inventory_id
        self.location_id = Inventory.objects.get(id=inventory_id).location_id
        self.employee = None
        self.status = self.ProductStatus.STORED
        return self.save()

    def pickup(self, employee_id: int) -> 'Product':
        """Product is picked up from a customer location or a inventory location. An employee is assigned to the inventory item."""
        if self.status == self.ProductStatus.DECOMMISSIONED:
            raise ProductStatusError('decommissioned inventory item cannot be picked up')
        if self.condition == self.Condition.NEW:
            self.condition = self.Condition.WORKING
        if self.employee_id == employee_id:
            raise InventoryLogicError('the same user cannot pick up an inventory item they are already holding')
        self.location = None
        self.employee_id = employee_id
        self.status = self.ProductStatus.PICKED_UP
        return self.save()

    def deploy(self, location_id: int) -> 'Product':
        """Deploys the inventory item at a customer location"""
        if self.status == self.ProductStatus.DECOMMISSIONED:
            raise ProductStatusError('decommissioned inventory item cannot be deployed')
        if self.status != self.ProductStatus.PICKED_UP:
            raise ProductStatusError('item must be picked up before it can be deployed')
        if self.condition in self.Condition.DAMAGED or self.Condition.IRREPARABLE:
            raise ProductConditionError('broken or irreparable item cannot be deployed')
        self.location_id = location_id
        self.status = self.ProductStatus.DEPLOYED
        return self.save()

    def decommission(self) -> 'Product':
        """Decommissions the item and removes all employee, inventory, and location associations"""
        notification_message: str = ''  # TODO  Add notification message for decommissioning an item.
        self.location = None
        self.employee = None
        self.inventory = None
        self.status = self.ProductStatus.DECOMMISSIONED
        return self.save()

    def save(self, *args, **kwargs):
        if self.inventory and not self.location:
            self.location_id = self.inventory.location_id
        return super().save(*args, **kwargs)


class Location(CreatedUpdatedModel):
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
        ordering = ('name',)


class CustomerLocation(models.Model):
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)


class Inventory(CreatedUpdatedModel):
    """A holder for all inventory items"""

    class InventoryStatus(models.TextChoices):
        """Choices for setting the status of a inventory location
        Active: Available for picking up and dropping off items
        Inactive: Not in use. Products cannot be picked up or dropped off from this location
        Full: The inventory location is currently full. No items can be dropped off.
        """

        ACTIVE = 'ACTIVE', _('Active')
        INACTIVE = 'INACTIVE', _('Inactive')
        FULL = 'FULL', _('Full')

    name = models.CharField(max_length=150, blank=True)
    status = models.CharField(max_length=16, choices=InventoryStatus.choices, default=InventoryStatus.ACTIVE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    editor = CurrentUserField(get_user_model(), related_name='inventory_editor', on_delete=models.CASCADE)
    creator = models.ForeignKey(get_user_model(), related_name='inventory_creator', on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse_lazy('inventory:inventory_detail', kwargs={'pk': self.pk})


class ProductType(models.Model):
    name = models.CharField(max_length=150)
    short_name = models.SlugField(unique=True)

    def __str__(self):
        return f'{self.name} ({self.short_name})'


class Notification(models.Model):
    """TODO  Implement this class"""
    pass


class NotificationPreference(models.Model):
    """TODO  Implement this class"""
    pass


@receiver(post_save, sender=Product)
def set_default_warehouse(sender, instance: Product, created, **kwargs):
    instance.inventory_id = 1


class Job(CreatedUpdatedModel):
    """Model for scheduling jobs to allow easier assignment of inventory, services and products"""

    class JobStatus(models.TextChoices):
        ACTIVE = 'ACTIVE', _('Active')
        CANCELED = 'CANCELED', _('Canceled')
        COMPLETED = 'COMPLETED', _('Completed')

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(max_length=16, choices=JobStatus.choices, default=JobStatus.ACTIVE)
    employee = models.ManyToManyField(get_user_model(), related_name='job_employees')
    editor = CurrentUserField(related_name='job_editor', on_delete=models.CASCADE, on_update=True)
    creator = CurrentUserField(related_name='job_creator', on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    date = models.DateTimeField()
    history = HistoricalRecords()

    def save(self, **kwargs):
        # TODO Implement a method that only allows updates if the job is in active status.
        print(kwargs)
        # if self.status == self.JobStatus.ACTIVE:
        return super().save(**kwargs)

    def __str__(self):
        return f'Job {self.id} for {self.customer} @ {self.date}'

    @property
    def employees(self):
        return self.employee.all()