from django.db import models

class Schedule(models.Model):
    """
    Represents a schedule for a job or set of jobs.
    """

    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    recurrence_rule = models.CharField(max_length=100)
    jobs = models.ManyToManyField('orders.Job', blank=True, related_name='schedules')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Schedules'