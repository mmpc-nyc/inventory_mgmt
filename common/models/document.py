from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from common.services.docusign_service import DocusignService


class Document(models.Model):
    # TODO Implement the action functions using the DocusignService

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('declined', 'Declined'),
    )
    envelope_id = models.CharField(max_length=50, blank=True, null=True)
    sender = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='sent_documents')
    recipients = models.ManyToManyField('users.User', related_name='received_documents')
    document = models.FileField(upload_to='documents/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    date_created = models.DateTimeField(auto_now_add=True)
    date_sent = models.DateTimeField(blank=True, null=True)
    date_completed = models.DateTimeField(blank=True, null=True)
    message = models.TextField(blank=True)
    signature = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f'{self.sender.username} - {self.document.name}'

    class Meta:
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')

    def send_for_signature(self):
        docusign_service = DocusignService()
        envelope_id = docusign_service.create_envelope(self.document.path, self.sender.email, self.recipients.all())
        self.status = 'sent'
        self.date_sent = timezone.now()
        self.save()
        return envelope_id

    def get_envelope_status(self):
        docusign_service = DocusignService()
        envelope_status = docusign_service.get_envelope_status(self.envelope_id)
        self.status = envelope_status
        if envelope_status == 'completed':
            self.date_completed = timezone.now()
        self.save()
        return envelope_status

    def cancel_envelope(self):
        docusign_service = DocusignService()
        docusign_service.void_envelope(self.envelope_id)
        self.status = 'cancelled'
        self.save()

    def decline_envelope(self):
        docusign_service = DocusignService()
        docusign_service.decline_envelope(self.envelope_id)
        self.status = 'declined'
        self.save()
