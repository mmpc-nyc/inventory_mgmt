from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _


class PurchaseOrder(models.Model):
    class Status(models.TextChoices):
        NEW = 'New', _('New')
        AWAITING_INTERNAL_APPROVAL = 'Awaiting Internal Approval', _('Awaiting Internal Approval')
        AWAITING_VENDOR_APPROVAL = 'Awaiting Vendor Approval', _('Awaiting Vendor Approval')
        INTERNALLY_APPROVED = 'Internally Approved', _('Internally Approved')
        INTERNALLY_REJECTED = 'Internally Rejected', _('Internally Rejected')
        VENDOR_ACCEPTED = 'Vendor Accepted', _('Vendor Accepted')
        VENDOR_REJECTED = 'Vendor Rejected', _('Vendor Rejected')
        CANCELED = 'Canceled', _('Canceled')
        CLOSED = 'Closed', _('Closed')

    class FulfillmentStatus(models.TextChoices):
        FULFILLED = 'Fulfilled', _('Fulfilled')
        UNFULFILLED = 'Unfulfilled', _('Unfulfilled')
        PARTIALLY_FULFILLED = 'Partially Fulfilled', _('Partially Fulfilled')


    vendor = models.ForeignKey('inventory.Vendor', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey('users.User', related_name='created_purchase_orders', on_delete=models.CASCADE)
    approved_by = models.ForeignKey('users.User', related_name='approved_purchase_orders', on_delete=models.CASCADE,
                                    null=True, blank=True)
    status = models.CharField(max_length=32, choices=Status.choices, default=Status.NEW)

    def __str__(self):
        return f'{self.vendor} - {self.date}'

    @property
    def total_price(self):
        material_price = self.materials.aggregate(Sum('price'))['price__sum'] or 0
        equipment_price = self.equipments.aggregate(Sum('price'))['price__sum'] or 0
        total_price = material_price + equipment_price
        return total_price

    @property
    def fulfillment_status(self):
        total_requested = sum([item.quantity for item in self.materials.all()] + [item.quantity for item in self.equipments.all()])
        total_received = sum([item.received_quantity for item in self.materials.all()] + [item.checked_in_quantity for item in self.equipments.all()])

        if total_received == 0:
            return self.FulfillmentStatus.UNFULFILLED
        elif total_received == total_requested:
            return self.FulfillmentStatus.FULFILLED
        else:
            return self.FulfillmentStatus.PARTIALLY_FULFILLED

    class Meta:
        verbose_name = _('Purchase Order')
        verbose_name_plural = _('Purchase Orders')
        ordering = ['-date']


class PurchaseOrderItem(models.Model):
    quantity = models.DecimalField(max_digits=5, decimal_places=2)
    received_quantity = models.DecimalField(max_digits=5, decimal_places=2)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        abstract = True


class PurchaseOrderEquipmentItem(PurchaseOrderItem):
    equipment = models.ForeignKey('inventory.VendorEquipment', on_delete=models.CASCADE)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='equipments')

    def __str__(self):
        return f'{self.equipment} ({self.quantity})'

    def save(self, *args, **kwargs):
        self.price = self.equipment.current_price * self.quantity
        super().save(*args, **kwargs)


class PurchaseOrderMaterialItem(PurchaseOrderItem):
    material = models.ForeignKey('inventory.VendorMaterial', on_delete=models.CASCADE)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='materials')

    def __str__(self):
        return f'{self.material} ({self.quantity})'

    def save(self, *args, **kwargs):
        self.price = self.material.current_price * self.quantity
        super().save(*args, **kwargs)
