from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class Job(models.Model):
    """
    Represents a job that needs to be done by a technician.
    """

    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', _('Active')
        COMPLETED = 'COMPLETED', _('Completed')
        CANCELLED = 'CANCELLED', _('Cancelled')
        PENDING = 'PENDING', _('Pending')

    class SubStatus(models.TextChoices):
        ASSIGNED = 'ASSIGNED', _('Assigned')
        IN_PROGRESS = 'IN_PROGRESS', _('In Progress')
        FINISHED = 'FINISHED', _('Finished')
        SUSPENDED = 'SUSPENDED', _('Suspended')

    # Fields for the job itself
    name = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.ACTIVE)
    sub_status = models.CharField(max_length=50, choices=SubStatus.choices, default=SubStatus.ASSIGNED, blank=True, null=True)
    duration = models.PositiveIntegerField(blank=True, null=True)

    # Fields for the start end time of the job
    scheduled_start_time = models.DateTimeField()
    scheduled_end_time = models.DateTimeField()
    actual_start_time = models.DateTimeField(blank=True, null=True)
    actual_end_time = models.DateTimeField(blank=True, null=True)

    # Fields for the technician and customer
    technicians = models.ManyToManyField('users.User', related_name='technicians')
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE)

    # relationships with other models
    services = models.ManyToManyField('orders.Service', through='JobService', related_name='job_services')
    materials = models.ManyToManyField('inventory.Material', through='JobMaterial', related_name='job_materials')
    products = models.ManyToManyField('inventory.Material', through='JobProduct', related_name='job_products')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Job')
        verbose_name_plural = _('Jobs')

    def get_absolute_url(self):
        return reverse_lazy('job_detail', kwargs={'pk': self.pk})


class JobService(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    service = models.ForeignKey('orders.Service', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class JobMaterial(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    material = models.ForeignKey('inventory.Material', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class JobProduct(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    product = models.ForeignKey('inventory.Material', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)