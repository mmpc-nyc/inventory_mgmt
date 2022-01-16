from collections import defaultdict
from typing import Union

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.utils.functional import cached_property
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from phonenumber_field.modelfields import PhoneNumberField

from inventory.exceptions import OrderCompletionError, ProductConditionError


class Contact(models.Model):
    """Model for managing contacts that attach to customers and employees"""
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    emails = models.ManyToManyField('Email', through='ContactEmail', related_name='emails')
    phone_numbers = models.ManyToManyField('PhoneNumber', through='ContactPhoneNumber', related_name='phone_numbers')

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
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    company_name = models.CharField(max_length=150, blank=True, default='')
    contacts = models.ManyToManyField('Contact', through='CustomerContact', related_name='contact')
    locations = models.ManyToManyField('Location', through='CustomerLocation', related_name='location')
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
        DECOMMISSIONED = 'DECOMMISSIONED', _('Decommissioned')

    name = models.CharField(max_length=150, blank=True, null=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    status = models.CharField(max_length=32, choices=Status.choices, default=Status.STORED)
    stock = models.ForeignKey('Stock', on_delete=models.SET_NULL, blank=True, null=True)
    condition = models.ForeignKey('Condition', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='equipment_employee', on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True, blank=True)
    counter = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Equipment')
        verbose_name_plural = _('Equipment')

    def _check_for_repeat_action(self, order: 'Order', action: 'EquipmentTransactionAction'):
        last_order_transaction_for_this_equipment: 'EquipmentTransaction' = order.equipmenttransaction_set.filter(
            self).last()
        if last_order_transaction_for_this_equipment:
            if last_order_transaction_for_this_equipment.action == action:
                raise ValidationError('Cannot Perform the same action as the last action')

    def _execute(self, action: 'EquipmentTransactionAction', user: User, order: 'Order' = None,
                 condition: 'Condition' = None, stock: 'Stock' = None,
                 recipient: User = None) -> 'EquipmentTransaction':
        if not self.condition.has_action(action.name):
            raise ProductConditionError(_(f'This equipment in condition {self.condition} cannot use action {action}'))

        with transaction.atomic():
            self.save()
            stock = stock or self.stock
            condition = condition or self.condition
            return EquipmentTransaction.objects.create(action=action, equipment=self, user=user, condition=condition,
                                                       stock=stock, order=order, recipient=recipient)

    def decommission(self, user: User):
        action = EquipmentTransactionAction.DECOMMISSION
        condition = Condition.objects.get(name='Decommissioned')

        self.user = None
        self.status = self.Status.DECOMMISSIONED
        self.location = None
        self.stock = None
        self.condition = condition

        return self._execute(action=action, user=user, condition=condition)

    def collect(self, user: User, order: 'Order', condition: 'Condition' = None):
        action = EquipmentTransactionAction.COLLECT

        self.user = user
        self.status = self.Status.PICKED_UP
        return self._execute(action=action, user=user, order=order, condition=condition)

    def deploy(self, user: User, order: 'Order', condition: 'Condition' = None):
        action = EquipmentTransactionAction.DEPLOY

        self.status = self.Status.DEPLOYED
        self.location = order.location

        return self._execute(action=action, user=user, order=order, condition=condition)

    def store(self, user: User, stock: 'Stock' = None, condition: 'Condition' = None):
        action = EquipmentTransactionAction.STORE
        stock = stock or self.stock

        self.user = None
        self.location = stock.location
        self.status = self.Status.STORED
        self.location = None

        return self._execute(action=action, user=user, condition=condition)

    def transfer(self, recipient: User, condition: 'Condition' = None):
        action = EquipmentTransactionAction.TRANSFER
        user = self.user
        self.user = recipient

        return self._execute(action=action, user=user, recipient=recipient, condition=condition)

    def withdraw(self, user: User, condition: 'Condition' = None):
        action = EquipmentTransactionAction.WITHDRAW

        self.user = user
        self.status = self.Status.PICKED_UP
        self.location = None

        return self._execute(action=action, user=user, condition=condition)

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
    action_collect = models.BooleanField(verbose_name=_('collect'), default=False)
    action_decommission = models.BooleanField(verbose_name=_('decommission'), default=False)
    action_deploy = models.BooleanField(verbose_name=_('deploy'), default=False)
    action_store = models.BooleanField(verbose_name=_('store'), default=False)
    action_transfer = models.BooleanField(verbose_name=_('transfer'), default=False)
    action_withdraw = models.BooleanField(verbose_name=_('withdraw'), default=False)

    def __str__(self):
        return f'{self.name}'

    def has_action(self, action_name: str) -> bool:
        formatted_action_name = f'action_{action_name.lower()}'
        if hasattr(self, formatted_action_name):
            return getattr(self, formatted_action_name)
        return False

    class Meta:
        verbose_name = _('Condition')
        verbose_name_plural = _('Conditions')


class GenericProduct(models.Model):
    """A generic product container that relates to different versions of the same product.
    For example: a product having different brands or different sizes or colors
    """

    class Status(models.TextChoices):
        """Generic Product status choices
        Active: The generic product is available for all actions
        Inactive: The generic product is no longer active but is still stored in the inventory
        """
        ACTIVE = 'Active', _('Active')
        INACTIVE = 'Inactive', _('Inactive')

    category = TreeForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=150, unique=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.ACTIVE)

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
    """A unique identifier for a product consisting of name, brand, product type, and generic product"""

    class Status(models.TextChoices):
        """Product status choices
        TODO  Rethink this
        """
        ACTIVE = 'Active', _('Active')  # Can be used and allows purchasing of new equipment
        INACTIVE = 'Inactive', _('Inactive')  # The product is no longer active but is still stored in the inventory
        RECALL = 'Recall', _('Recall')  # The product is inactive and should no longer be used.

    name = models.CharField(max_length=150)
    generic_product = models.ForeignKey('GenericProduct', on_delete=models.CASCADE)
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

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Stock')
        verbose_name_plural = _('Stocks')

    def get_absolute_url(self):
        return reverse_lazy('stock:stock_detail', kwargs={'pk': self.pk})


class EquipmentTransactionAction(models.TextChoices):
    COLLECT = 'Collect', _('Collect')
    DECOMMISSION = 'Decommission', _('Decommission')
    DEPLOY = 'Deploy', _('Deploy')
    STORE = 'Store', _('Store')
    TRANSFER = 'Transfer', _('Transfer')
    WITHDRAW = 'Withdraw', _('Withdraw')


class EquipmentTransactionManager(models.Manager):
    ...


class EquipmentTransaction(models.Model):
    """A model for managing equipment transactions. Mainly used for logging and auditing"""
    action = models.CharField(max_length=32, choices=EquipmentTransactionAction.choices)
    equipment = models.ForeignKey(Equipment, verbose_name=_('equipment'), on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), verbose_name=_('user'), on_delete=models.CASCADE)
    recipient = models.ForeignKey(get_user_model(), verbose_name=_('recipient'), related_name='recipient',
                                  on_delete=models.CASCADE, blank=True, null=True)
    stock = models.ForeignKey('Stock', verbose_name=_('stock'), on_delete=models.CASCADE, blank=True, null=True)
    condition = models.ForeignKey(Condition, verbose_name=_('condition'), on_delete=models.CASCADE)
    timestamp = models.DateTimeField(verbose_name=_('timestamp'), auto_now=True)
    location = models.ForeignKey('Location', verbose_name=_('Location'), blank=True, null=True,
                                 on_delete=models.CASCADE)
    order = models.ForeignKey('Order', verbose_name=_('Order'), blank=True, null=True, on_delete=models.CASCADE)

    objects = EquipmentTransactionManager()

    def clean(self):
        super().clean()

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = _('Equipment Transaction')
        verbose_name_plural = _('Equipment Transactions')


class OrderActivity(models.TextChoices):
    DEPLOY = 'Deploy', _('Deploy')
    COLLECT = 'Collect', _('Collect')
    INSPECT = 'Inspect', _('Inspect')


class OrderManager(models.Manager):
    activity: OrderActivity

    def get_queryset(self):
        qs = super().get_queryset()
        if hasattr(self, 'activity'):
            return qs.filter(activity=self.activity)
        return qs

    def create(self, **kwargs):
        if hasattr(self, 'activity'):
            kwargs.update({'activity': self.activity})
        return super().create(**kwargs)


class CollectOrderManager(OrderManager):
    activity = OrderActivity.COLLECT


class DeployOrderManager(OrderManager):
    activity = OrderActivity.DEPLOY


class InspectOrderManager(OrderManager):
    activity = OrderActivity.INSPECT


class Order(models.Model):
    """Model for scheduling orders to allow easier assignment of inventory, services and products"""

    Activity: OrderActivity = OrderActivity

    class Status(models.TextChoices):
        NEW = 'New', _('New')
        ASSIGNED = 'Assigned', _('Assigned')
        IN_PROGRESS = 'In Progress', _('In Progress')
        COMPLETED = 'Completed', _('Completed')
        CANCELED = 'Canceled', _('Canceled')

    parent = models.ManyToManyField('self', related_name='children', symmetrical=False)
    customer = models.ForeignKey(Customer, verbose_name=_('customer'), on_delete=models.CASCADE)
    activity = models.CharField(verbose_name=_('activity'), max_length=32, choices=Activity.choices)
    status = models.CharField(max_length=16, verbose_name=_('status'), choices=Status.choices, default=Status.NEW)
    users = models.ManyToManyField(get_user_model(), verbose_name=_('users'), related_name='order_users')
    location = models.ForeignKey(Location, verbose_name=_('location'), on_delete=models.CASCADE)
    date = models.DateTimeField()
    equipments = models.ManyToManyField('Equipment', verbose_name=_('equipments'), through='OrderEquipment',
                                        related_name='equipments')
    generic_products = models.ManyToManyField('GenericProduct', verbose_name=_('generic products'),
                                              through='OrderGenericProduct', related_name='generic_products')

    objects = OrderManager()

    def complete(self, ignore_issues: bool = False) -> None:
        self.status = Order.Status.COMPLETED
        self.save()

    def cancel(self, ignore_issues: bool = False):
        self.status = Order.Status.COMPLETED
        self.save()

    def save(self, **kwargs):
        # TODO Implement a method that only allows updates if the order is in active status.
        return super().save(**kwargs)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return f'{self.id}'


class CollectOrder(Order):
    objects = CollectOrderManager()

    def complete(self, ignore_issues: bool = False) -> None:
        # equipment_dict = defaultdict(dict)
        # for equipment_transaction in self.equipmenttransaction_set.all():
        #     if self.equipments.count() != order_equipment_transactions
        #         if deployed_equipment:
        #             if not ignore_issues:
        #                 raise OrderCompletionError('Not all equipment has been picked up')
        # deployed_equipment.update(equipment__status=Equipment.Status.MISSING)

        super().complete(ignore_issues=ignore_issues)

    class Meta:
        proxy = True


class DeployOrder(Order):
    objects = DeployOrderManager()

    def complete(self, ignore_issues: bool = False) -> None:
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

        super().complete(ignore_issues=ignore_issues)

    class Meta:
        proxy = True


class InspectOrder(Order):
    objects = InspectOrderManager()

    class Meta:
        proxy = True


class OrderFactory:
    activity: OrderActivity

    def create_from_orders(self, date, orders: Union[Order, list[Order], tuple[Order], QuerySet]) -> Order:
        if isinstance(orders, Order):
            orders = [orders]
        equipments = set()
        for order in orders:
            for equipment in order.equipments.all():
                equipments.add(equipment)  # TODO Think about broken / decommissioned equipment
        with transaction.atomic():
            order = Order(activity=self.activity, date=date, status=Order.Status.NEW, customer=orders[0].customer,
                          location=orders[0].location)
            for equipment in equipments:
                order.equipmenttransaction_set.add(equipment)
            order.save()
            return order

    def create_from_equipment(self, date, customer, location, equipments: Union[
        Equipment, list[Equipment], tuple[Equipment], set[Equipment], QuerySet] = None) -> Order:
        if equipments:
            if isinstance(equipments, Equipment):
                equipments = [equipments]
        with transaction.atomic():
            order = Order(activity=self.activity, date=date, status=Order.Status.NEW, customer=customer,
                          location=location)
            for equipment in equipments:
                order.equipmenttransaction_set.add(equipment)
            order.save()
            return order


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
    # TODO Create order transactions that keep track of when equipment was picked up.

    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    equipment = models.ForeignKey('Equipment', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.order} | {self.equipment}'

    class Meta:
        verbose_name = _('Order Equipment')
        verbose_name_plural = _('Order Equipment')
        unique_together = ('order', 'equipment')
