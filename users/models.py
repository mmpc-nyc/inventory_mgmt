from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from inventory.models.location import Location


class User(AbstractUser):
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.username}'

    def get_name_or_username(self) -> str:
        return ' '.join(
            name for name in [self.first_name, self.last_name] if name
        ) or self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username}'

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')


