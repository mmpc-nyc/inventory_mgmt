from django.db import models
from django.utils.translation import gettext_lazy as _


# TODO  Fix the warranty model. This doesn't work properly
class Warranty(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Warranty')
        verbose_name_plural = _('Warranties')
