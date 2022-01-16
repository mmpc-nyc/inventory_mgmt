from collections import defaultdict

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from inventory.enums import OrderActivity
from inventory.exceptions import OrderCompletionError
from inventory.managers.order import OrderManager, DeployOrderManager, InspectOrderManager
from inventory.models.equipment import Equipment
from inventory.models.location import Location
from inventory.models.customer import Customer


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

    def perform_equipment_activity(self, user:get_user_model(), equipment: Equipment):
        ...

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

    def perform_equipment_activity(self, user: get_user_model(), equipment: Equipment):
        equipment.collect(user, equipment)
        super().perform_equipment_activity(user, equipment)

    def complete(self, ignore_issues: bool = False) -> None:
        equipment_dict = defaultdict(dict)
        print(self.equipmenttransaction_set.filter(equipment__in=self.equipmenttransaction_set.all()))
        for equipment_transaction in self.equipmenttransaction_set.all():
            print(equipment_transaction)
        #         if deployed_equipment:
        #             if not ignore_issues:
        #                 raise OrderCompletionError('Not all equipment has been picked up')
        # deployed_equipment.update(equipment__status=Equipment.Status.MISSING)

        super().complete(ignore_issues=ignore_issues)

    class Meta:
        proxy = True


class DeployOrder(Order):
    objects = DeployOrderManager()

    def perform_equipment_activity(self, user: get_user_model(), equipment: Equipment):
        equipment.deploy(user, equipment)
        super().perform_equipment_activity(user, equipment)

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

    def perform_equipment_activity(self, user: get_user_model(), equipment: Equipment):
        equipment.inspect(user, equipment)
        super().perform_equipment_activity(user, equipment)

    class Meta:
        proxy = True


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