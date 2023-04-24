from django.db import models
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

    vendor = models.ForeignKey('inventory.Vendor', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey('users.User', related_name='created_purchase_orders', on_delete=models.CASCADE)
    approved_by = models.ForeignKey('users.User', related_name='approved_purchase_orders', on_delete=models.CASCADE,
                                    null=True, blank=True)
    status = models.CharField(max_length=32, choices=Status.choices, default=Status.NEW)

    def __str__(self):
        return f'{self.vendor} - {self.date_created}'

    class Meta:
        verbose_name = _('Purchase Order')
        verbose_name_plural = _('Purchase Orders')
        ordering = ['-date']


class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey('inventory.VendorItem', on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=5, decimal_places=2)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.item} ({self.quantity})'

    def save(self, *args, **kwargs):
        self.price = self.item.current_price * self.quantity
        super().save(*args, **kwargs)