from test_base import AbstractTest


class AbstractTestHolder:
    class AbstractOrderManager(AbstractTest):
        def test_create(self):
            self.fail()

        def test_all(self):
            self.fail()


class TestInspectOrderManager(AbstractTestHolder.AbstractOrderManager):
    ...


class TestDeployOrderManager(AbstractTestHolder.AbstractOrderManager):
    ...


class TestOrderManager(AbstractTestHolder.AbstractOrderManager):
    ...


class TestCollectOrderManager(AbstractTestHolder.AbstractOrderManager):

    def test_create_from_one_order(self):
        self.fail()

    def test_create_from_multiple_orders(self):
        self.fail()

    def test_create_using_equipment(self):
        self.fail()
