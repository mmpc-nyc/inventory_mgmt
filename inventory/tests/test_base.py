from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from inventory.models.customer import Customer, CustomerLocation
from inventory.models.equipment import Condition, Equipment
from inventory.models.location import Location
from inventory.models.order import OrderGenericProduct, OrderEquipment, DeployOrder, CollectOrder, InspectOrder
from inventory.models.product import ProductType, GenericProduct, Product, Brand
from inventory.models.stock import Stock

User = get_user_model()


class AbstractTest(TestCase):
    fixtures = ['fixtures/db.json', ]

    def setUp(self):
        self.user = User.objects.create(username='user', password='user')
        self.recipient = User.objects.create(username='recipient', password='recipient', )
        self.location_stock = Location.objects.create(raw='Stock Location')
        self.location_customer_1 = Location.objects.create(raw='Customer Location 1')
        self.location_customer_2 = Location.objects.create(raw='Customer Location 2')
        self.location_user = Location.objects.create(raw='User Location')
        self.stock = Stock.objects.create(name='Stock 1', location=self.location_stock)
        self.customer_1 = Customer.objects.create(first_name='Test', last_name='Customer 1')
        self.customer_2 = Customer.objects.create(first_name='Test', last_name='Customer 2')
        self.customer_1_location_1 = CustomerLocation.objects.create(customer=self.customer_1,
                                                                     location=self.location_customer_1)
        self.customer_location_2 = CustomerLocation.objects.create(customer=self.customer_2,
                                                                   location=self.location_customer_2)
        self.brand = Brand.objects.create(name='Brand 1')
        self.product_type_equipment = ProductType.objects.create(name='Equipment')
        self.generic_product = GenericProduct.objects.create(name='Generic Product 1')
        self.product = Product.objects.create(
            name='Product 1',
            generic_product=self.generic_product,
            brand=self.brand,
            product_type=self.product_type_equipment
        )
        self.condition_working = Condition.objects.get(name='Working')
        self.condition_damaged = Condition.objects.get(name='Damaged')
        self.condition_decommissioned = Condition.objects.get(name='Decommissioned')
        self.equipment_stored_working = Equipment.objects.create(
            name='stored_working',
            product=self.product,
            condition=self.condition_working,
            stock=self.stock,
            location=self.stock.location
        )
        self.equipment_picked_up_working_1 = Equipment.objects.create(
            name='picked_up_working_1',
            product=self.product,
            condition=self.condition_working,
            stock=self.stock,
            location=self.location_user,
            user=self.user,
            status=Equipment.Status.PICKED_UP
        )
        self.equipment_picked_up_working_2 = Equipment.objects.create(
            name='picked_up_working_2',
            product=self.product,
            condition=self.condition_working,
            stock=self.stock,
            location=self.location_user,
            user=self.user,
            status=Equipment.Status.PICKED_UP
        )
        self.equipment_deployed_working_1 = Equipment.objects.create(
            name='deployed_working_1',
            product=self.product,
            condition=self.condition_working,
            stock=self.stock,
            status=Equipment.Status.DEPLOYED
        )
        self.equipment_deployed_working_2 = Equipment.objects.create(
            name='deployed_working_2',
            product=self.product,
            condition=self.condition_working,
            stock=self.stock,
            status=Equipment.Status.DEPLOYED
        )

        self.order_deploy_initial = DeployOrder.objects.create(
            customer=self.customer_1,
            location=self.customer_1_location_1.location,
            date=timezone.now(),
        )
        self.order_deploy_partial = DeployOrder.objects.create(
            customer=self.customer_1,
            location=self.customer_1_location_1.location,
            date=timezone.now(),
        )
        self.order_deploy_complete = DeployOrder.objects.create(
            customer=self.customer_1,
            location=self.customer_1_location_1.location,
            date=timezone.now(),
        )
        OrderGenericProduct.objects.create(
            order=self.order_deploy_initial,
            generic_product=self.generic_product,
            quantity=2
        )
        OrderGenericProduct.objects.create(
            order=self.order_deploy_partial,
            generic_product=self.generic_product,
            quantity=2
        )
        OrderGenericProduct.objects.create(
            order=self.order_deploy_complete,
            generic_product=self.generic_product,
            quantity=2
        )
        OrderEquipment.objects.create(order=self.order_deploy_partial, equipment=self.equipment_deployed_working_1)
        OrderEquipment.objects.create(order=self.order_deploy_complete, equipment=self.equipment_deployed_working_1)
        OrderEquipment.objects.create(order=self.order_deploy_complete, equipment=self.equipment_deployed_working_2)

        self.order_collect_initial = CollectOrder.objects.create(
            customer=self.customer_1,
            location=self.customer_1_location_1.location,
            date=timezone.now()
        )
        self.order_collect_partial = CollectOrder.objects.create(
            customer=self.customer_1,
            location=self.customer_1_location_1.location,
            date=timezone.now()
        )
        self.order_collect_complete = CollectOrder.objects.create(
            customer=self.customer_1,
            location=self.customer_1_location_1.location,
            date=timezone.now()
        )
        OrderEquipment.objects.create(order=self.order_collect_initial, equipment=self.equipment_deployed_working_1)
        OrderEquipment.objects.create(order=self.order_collect_initial, equipment=self.equipment_deployed_working_2)
        OrderEquipment.objects.create(order=self.order_collect_partial, equipment=self.equipment_picked_up_working_1)
        OrderEquipment.objects.create(order=self.order_collect_partial, equipment=self.equipment_deployed_working_2)
        OrderEquipment.objects.create(order=self.order_collect_complete, equipment=self.equipment_picked_up_working_1)
        OrderEquipment.objects.create(order=self.order_collect_complete, equipment=self.equipment_picked_up_working_2)

        self.order_inspect = InspectOrder.objects.create(
            customer=self.customer_1,
            location=self.customer_1_location_1.location,
            date=timezone.now())
