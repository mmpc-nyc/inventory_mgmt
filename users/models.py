from django.contrib.auth.models import AbstractUser
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


