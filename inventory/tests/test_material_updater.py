from inventory.utils.epa_scraper import MaterialUpdater
from unittest import TestCase


class TestMaterialUpdater(TestCase):
    updater = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.updater = MaterialUpdater()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.updater.close()

    def test_create_or_update_pesticide(self):
        print(self.updater.create_or_update_pesticide('9444-158', 'Clean Air Purge III'))
