from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
from .customer_models import Customer
from .location_models import Location
from .helper_models import CreatedUpdatedModel
from django_currentuser.db.models import CurrentUserField
from django.db import models


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