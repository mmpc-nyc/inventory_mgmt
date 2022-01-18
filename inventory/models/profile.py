from django.db import models
from django.utils.translation import gettext_lazy as _

from inventory.models.location import Location
from users.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f'{self.user.username}'

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')