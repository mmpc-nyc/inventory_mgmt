from django.db import models
from django.utils.translation import gettext_lazy as _


class OrderActivity(models.TextChoices):
    DEPLOY = 'Deploy', _('Deploy')
    COLLECT = 'Collect', _('Collect')
    INSPECT = 'Inspect', _('Inspect')