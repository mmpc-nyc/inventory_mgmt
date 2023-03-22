from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class Transfer(models.Model):
    """
        Model for a Transfer
        A transfer represents the movement of a quantity of an item (either equipment or material)
        from a source location (e.g. a technician, a vehicle, or a stock location) to a destination location.
    """
    class TransferStatus(models.TextChoices):
        PENDING = 'Pending', _('Pending')
        IN_TRANSIT = 'In Transit', _('In Transit')
        COMPLETED = 'Completed', _('Completed')

    source_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='source_transfers')
    source_id = models.PositiveIntegerField()
    source = GenericForeignKey('source_type', 'source_id')

    destination_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='destination_transfers')
    destination_id = models.PositiveIntegerField()
    destination = GenericForeignKey('destination_type', 'destination_id')

    agent = models.ForeignKey('users.User', verbose_name=_('Transfer Agent'), on_delete=models.SET_NULL,
                                       null=True, blank=True)
    status = models.CharField(verbose_name=_('Transfer Status'), max_length=16, choices=TransferStatus.choices,
                                       default=TransferStatus.PENDING)
    transfer_start_date = models.DateTimeField(verbose_name=_('Transfer Start Date'), null=True, blank=True)
    transfer_end_date = models.DateTimeField(verbose_name=_('Transfer End Date'), null=True, blank=True)
    transfer_notes = models.TextField(verbose_name=_('Transfer Notes'), blank=True)
    receiving_agent = models.ForeignKey('users.User', verbose_name=_('Receiving Agent'), on_delete=models.SET_NULL,
                                        null=True, blank=True, related_name='received_transfers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Transfer')
        verbose_name_plural = _('Transfers')

    def __str__(self):
        return f'Transfer from {self.source} to {self.destination}'

    def save(self, *args, **kwargs):
        if self.transfer_end_date and not self.receiving_agent:
            raise ValueError("A receiving agent must be specified to complete the transfer")
        super().save(*args, **kwargs)


class TransferItem(models.Model):
    transfer = models.ForeignKey(Transfer, on_delete=models.CASCADE, related_name='transfer_items')
    equipment_item = models.ForeignKey('inventory.EquipmentItem', on_delete=models.CASCADE, null=True, blank=True)
    material_stock = models.ForeignKey('inventory.MaterialStock', on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField()


class TransferAcceptance(models.Model):
    transfer = models.ForeignKey(Transfer, on_delete=models.CASCADE)
    accepted_by = models.ForeignKey('users.User', on_delete=models.CASCADE)
    accepted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Transfer Acceptance')
        verbose_name_plural = _('Transfer Acceptances')


class TransferItemAcceptance(models.Model):
    transfer_acceptance = models.ForeignKey(TransferAcceptance, on_delete=models.CASCADE, related_name='item_acceptances')
    transfer_item = models.ForeignKey(TransferItem, on_delete=models.CASCADE, related_name='acceptances')
    accepted_by = models.ForeignKey('users.User', on_delete=models.CASCADE)
    accepted_at = models.DateTimeField(auto_now_add=True)
    accepted_quantity = models.IntegerField()

    class Meta:
        verbose_name = _('Transfer Item Acceptance')
        verbose_name_plural = _('Transfer Item Acceptances')


@receiver(post_save, sender=Transfer)
def create_transfer_acceptance(sender, instance, created, **kwargs):
    if created:
        TransferAcceptance.objects.create(transfer=instance)
