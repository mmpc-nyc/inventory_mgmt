from django.test import TestCase
from django.contrib.auth import get_user_model

from inventory.models import Equipment

User = get_user_model()


class TestEquipment(TestCase):
    user: User
    fixtures = ['fixtures/db.json', ]

    def setUp(self) -> None:
        super().setUp()
        self.lost_missing_no_user = Equipment.objects.get(pk=1)
        self.decommissioned_picked_up_user = Equipment.objects.get(pk=32)
        self.working_picked_up_no_user = Equipment.objects.get(pk=7)
        self.working_picked_up_user_1 = Equipment.objects.get(pk=8)
        self.working_picked_up_user_2 = Equipment.objects.get(pk=9)