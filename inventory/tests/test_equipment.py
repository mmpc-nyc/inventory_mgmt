from django.db import IntegrityError
from django.test import TestCase

from inventory.exceptions import ProductStatusError, ProductConditionError
from django.contrib.auth import get_user_model

from inventory.models import Equipment

User = get_user_model()


class TestEquipment(TestCase):
    user: User
    fixtures = ['fixtures/test.json', ]

    def setUp(self) -> None:
        super().setUp()
        self.lost_missing_no_user = Equipment.objects.get(pk=1)
        self.decommissioned_picked_up_user = Equipment.objects.get(pk=32)
        self.working_picked_up_no_user = Equipment.objects.get(pk=7)
        self.working_picked_up_user_1 = Equipment.objects.get(pk=8)
        self.working_picked_up_user_2 = Equipment.objects.get(pk=9)

    def test_deploy_no_order(self):
        with self.assertRaises(TypeError):
            self.lost_missing_no_user.deploy()

    def test_deploy_status(self):
        with self.assertRaises(ProductStatusError):
            self.lost_missing_no_user.deploy(1)

    def test_deploy_condition(self):
        with self.assertRaises(ProductConditionError):
            self.decommissioned_picked_up_user.deploy(1)

    def test_deploy_user(self):
        self.working_picked_up_user_1.deploy(1)
        self.working_picked_up_user_2.deploy(1)
        with self.assertRaises(IntegrityError):
            self.working_picked_up_no_user.deploy(1)