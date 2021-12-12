from django.contrib.auth import get_user_model
from django.db import models
from .location_models import Location

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django_currentuser.db.models import CurrentUserField
from simple_history.models import HistoricalRecords

from inventory.exceptions import ItemStatusError, ItemConditionError, InventoryLogicError
from inventory.models.helper_models import CreatedUpdatedModel
from inventory.models.job_models import Job

User = get_user_model()


class Storage(CreatedUpdatedModel):
    """A holder for all inventory items"""

    class StorageStatus(models.TextChoices):
        """Choices for setting the status of a storage location
        Active: Available for picking up and dropping off items
        Inactive: Not in use. Items cannot be picked up or dropped off from this location
        Full: The storage location is currently full. No items can be dropped off.
        """

        ACTIVE = 'ACTIVE', _('Active')
        INACTIVE = 'INACTIVE', _('Inactive')
        FULL = 'FULL', _('Full')

    name = models.CharField(max_length=150, blank=True)
    status = models.CharField(max_length=16, choices=StorageStatus.choices, default=StorageStatus.ACTIVE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    editor = CurrentUserField(User, related_name='inventory_editor', on_delete=models.CASCADE)
    creator = models.ForeignKey(User, related_name='inventory_creator', on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.name}'


class Item(CreatedUpdatedModel):
    """An item that can be inventoried"""

    class ItemStatus(models.TextChoices):
        """Item status choices
        Stored: Item stored in Storage
        Deployed: Item deployed at customer location
        Decommissioned: Item no longer in use and not in inventory
        Picked Up: Item is currently with the employee. Not at any customer location or storage.
        """
        STORED = 'STORED', _('Stored')
        DEPLOYED = 'DEPLOYED', _('Deployed')
        DECOMMISSIONED = 'DECOMMISSIONED', _('Decommissioned')
        PICKED_UP = 'PICKED_UP', _('Picked Up')

    class ItemCondition(models.TextChoices):
        """Current condition of an item.
        New: Brand new item that has not been used. When the item is picked up it is automatically changed to working.
        Working: Item is in good working condition
        Damaged: Item is damaged and needs repair
        Irreparable: Item is damaged beyond repair. This item should be decommissioned
        """
        NEW = 'NEW', _('New')
        WORKING = 'WORKING', _('Working')
        DAMAGED = 'DAMAGED', _('Damaged')
        IRREPARABLE = 'IRREPARABLE', _('Irreparable')

    class ItemNotificationMessage:
        """Possible class for selecting different kinds of item based notification messages"""

    name = models.CharField(max_length=150)
    label = models.CharField(max_length=150, null=True, blank=True)
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=16, choices=ItemStatus.choices, default=ItemStatus.STORED)
    employee = models.ForeignKey(User, related_name='inventory_item_employee', on_delete=models.SET_NULL, null=True, blank=True)
    editor = CurrentUserField(related_name='inventory_item_editor', on_delete=models.SET_NULL, on_update=True)
    creator = CurrentUserField(related_name='inventory_item_creator', on_delete=models.SET_NULL)
    condition = models.CharField(max_length=16, choices=ItemCondition.choices, default=ItemCondition.NEW)
    storage = models.ForeignKey('Storage', on_delete=models.SET_NULL, blank=True, null=True)
    location = models.ForeignKey('Location', on_delete=models.SET_NULL, blank=True, null=True)
    item_type = models.ForeignKey('ItemType', on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.name}'

    def store(self, storage_id: int = None) -> 'Item':
        """Stores the item at a storage location. By default the item is returned to it's original location.
        If a storage_id is supplied the item is moved to a new storage location with the given storage_id"""
        if self.status == self.ItemStatus.DECOMMISSIONED:
            raise ItemStatusError('decommissioned item cannot be stored')
        if storage_id is None and self.storage_id is None:
            raise InventoryLogicError('the current item does not have a storage associated with it. A storage_id must '
                                      'be passed')
        if self.status == Item.ItemStatus.STORED and type(self.storage_id) != type(None) and type(storage_id) != type(None) and int(self.storage_id) == int(storage_id):
            raise InventoryLogicError('cannot store item in a location it is already stored in')
        if storage_id is not None:
            self.storage_id = storage_id
        self.location_id = Storage.objects.get(id=storage_id).location_id
        self.employee = None
        self.status = self.ItemStatus.STORED
        return self.save()

    def pickup(self, employee_id: int) -> 'Item':
        """Item is picked up from a customer location or a storage location. An employee is assigned to the item."""
        if self.status == self.ItemStatus.DECOMMISSIONED:
            raise ItemStatusError('decommissioned item cannot be picked up')
        if self.condition == self.ItemCondition.NEW:
            self.condition = self.ItemCondition.WORKING
        if self.employee_id == employee_id:
            raise InventoryLogicError('the same user cannot pick up an item they are already holding')
        self.location = None
        self.employee_id = employee_id
        self.status = self.ItemStatus.PICKED_UP
        return self.save()

    def deploy(self, location_id: int) -> 'Item':
        """Deploys the item at a customer location"""
        if self.status == self.ItemStatus.DECOMMISSIONED:
            raise ItemStatusError('decommissioned item cannot be deployed')
        if self.status != self.ItemStatus.PICKED_UP:
            raise ItemStatusError('item must be picked up before it can be deployed')
        if self.condition in self.ItemCondition.DAMAGED or self.ItemCondition.IRREPARABLE:
            raise ItemConditionError('broken or irreparable item cannot be deployed')
        self.location_id = location_id
        self.status = self.ItemStatus.DEPLOYED
        return self.save()

    def decommission(self) -> 'Item':
        """Decommissions the item and removes all employee, storage, and location associations"""
        notification_message: str = ''  # TODO  Add notification message for decommissioning an item.
        self.location = None
        self.employee = None
        self.storage = None
        self.status = self.ItemStatus.DECOMMISSIONED
        return self.save()

    def save(self, *args, **kwargs):
        if self.storage and not self.location:
            self.location_id = self.storage.location_id
        return super().save(*args, **kwargs)


class ItemType(models.Model):
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


@receiver(post_save, sender=Item)
def set_default_warehouse(sender, instance: Item, created, **kwargs):
    instance.storage_id = 1