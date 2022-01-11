from django.test import TestCase

from inventory.actions import DeployAction
from inventory.models import Equipment


class TestStoreAction(TestCase):

    fixtures = ['fixtures/db.json',]

    def setUp(self) -> None:
        self.equipment_working_picked_up = Equipment.objects.get(id=7)
        super().setUp()

    def test_execute(self):

        action = DeployAction(
            equipment = self.equipment_working_picked_up,
            user= self.equipment_working_picked_up.user,
            stock = self.equipment_working_picked_up.stock,
        )
        res = action.execute()