from unittest import TestCase


class TestEquipment(TestCase):

    fixtures = ['test.json',]

    def setUp(self) -> None:
        super().setUp()

    def test_decommission(self):
        print('hi')
