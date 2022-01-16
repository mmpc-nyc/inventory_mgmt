from collections import defaultdict
from typing import Union

from django.contrib.auth import get_user_model
from django.db import models, transaction
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

from inventory.exceptions import OrderCompletionError
from inventory.models.location import Location
from inventory.models.customer import Customer
from inventory.models.equipment import Equipment


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
    activity = OrderActivity.COLLECT

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