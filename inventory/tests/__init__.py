from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from inventory.models.contact import Contact, Email, PhoneNumber
from inventory.models.customer import Customer, ServiceLocation
from inventory.models.location import Location
from inventory.models.order import Condition, Equipment, Order, CollectOrder, OrderEquipment, DeployOrder, \
    OrderGenericProduct, InspectOrder
from inventory.models.product import Brand, ProductType, GenericProduct, Product
from inventory.models.warehouse import Warehouse

User = get_user_model()


class AbstractTest(TestCase):
    fixtures = ['fixtures/test.json', ]

    def setUp(self):
        self.user = User.objects.create(username='user', password='user')
        self.recipient = User.objects.create(username='recipient', password='recipient', )
        self.customer_email = "customer@email.com"
        self.customer_phone = "2122198218"
        self.customer_contact = Contact.objects.create(first_name="Customer", last_name="contact")
        self.location_warehouse = Location.objects.create(
            name='Warehouse Location 1',
            address_line_1='Warehouse Location 1',
            city="Warehouse City",
            state="Warehouse State",
            postal_code="00000",
            latitude=0,
            longitude=0, )
        self.location_customer_1 = Location.objects.create(
            name='Customer Location 1',
            address_line_1='Customer Location 1',
            city="Customer City",
            state="Customer State",
            postal_code="00000",
            latitude=0,
            longitude=0,
        )
        self.location_customer_2 = Location.objects.create(
            name='Customer Location 2',
            address_line_1='Customer Location 2',
            city="Customer City",
            state="Customer State",
            postal_code="00000",
            latitude=0,
            longitude=0,
        )
        self.location_user = Location.objects.create(
            name='User Location 2',
            address_line_1='User Location 2',
            city="User City",
            state="User State",
            postal_code="00000",
            latitude=0,
            longitude=0, )
        self.warehouse = Warehouse.objects.create(name='Warehouse 1', location=self.location_warehouse)
        self.billing_location_1 = Location.objects.create(
            name='Billing Location 1',
            address_line_1='Billing Location 1',
            city="Billing City",
            state="Billing State",
            postal_code="00000",
            latitude=0,
            longitude=0
        )
        self.billing_location_2 = Location.objects.create(
            name='Billing Location 1',
            address_line_1='Billing Location 1',
            city="Billing City",
            state="Billing State",
            postal_code="00000",
            latitude=0,
            longitude=0)
        self.customer_1 = Customer.objects.create(
            first_name='Test',
            last_name='Customer 1',
            email=self.customer_email,
            phone_number=self.customer_phone,
            billing_location=self.billing_location_1
        )
        self.customer_2 = Customer.objects.create(
            first_name='Test',
            last_name='Customer 2',
            billing_location=self.billing_location_2,
            email=self.customer_email,
            phone_number=self.customer_phone,
        )
        self.customer_1_location_1 = ServiceLocation.objects.create(customer=self.customer_1,
                                                                    location=self.location_customer_1)
        self.customer_location_2 = ServiceLocation.objects.create(customer=self.customer_2,
                                                                  location=self.location_customer_2)
        self.brand = Brand.objects.create(name='Brand 1')
        self.generic_product = GenericProduct.objects.create(name='Generic Product 1')
        self.product = Product.objects.create(
            name='Product 1',
            generic_product=self.generic_product,
            brand=self.brand,
        )
        self.condition_working = Condition.objects.get(name='Working')
        self.condition_damaged = Condition.objects.get(name='Damaged')
        self.condition_decommissioned = Condition.objects.get(name='Decommissioned')
        self.equipment_stored_working = Equipment.objects.create(
            name='stored_working',
            product=self.product,
            condition=self.condition_working,
            warehouse=self.warehouse,
            location=self.warehouse.location
        )
        self.equipment_picked_up_working_1 = Equipment.objects.create(
            name='picked_up_working_1',
            product=self.product,
            condition=self.condition_working,
            warehouse=self.warehouse,
            location=self.location_user,
            user=self.user,
            status=Equipment.Status.PICKED_UP
        )
        self.equipment_picked_up_working_2 = Equipment.objects.create(
            name='picked_up_working_2',
            product=self.product,
            condition=self.condition_working,
            warehouse=self.warehouse,
            location=self.location_user,
            user=self.user,
            status=Equipment.Status.PICKED_UP
        )
        self.equipment_deployed_working_1 = Equipment.objects.create(
            name='deployed_working_1',
            product=self.product,
            condition=self.condition_working,
            warehouse=self.warehouse,
            status=Equipment.Status.DEPLOYED
        )
        self.equipment_deployed_working_2 = Equipment.objects.create(
            name='deployed_working_2',
            product=self.product,
            condition=self.condition_working,
            warehouse=self.warehouse,
            status=Equipment.Status.DEPLOYED
        )

        self.order_collect_initial = self.create_order_collect_initial()
        self.order_collect_partial = self.create_order_collect_partial()
        self.order_collect_complete = self.create_order_collect_complete()
        self.order_deploy_initial = self.create_order_deploy_initial()
        self.order_deploy_partial = self.create_order_deploy_partial()
        self.order_deploy_complete = self.create_order_deploy_complete()
        self.order_inspect = self.create_order_inspect()

    def create_order_collect_initial(self) -> Order:
        order = CollectOrder.objects.create(
            customer=self.customer_1,
            location=self.customer_1_location_1.location,
            date=timezone.now()
        )
        order_equipment_1 = OrderEquipment.objects.create(order=order, equipment=self.equipment_deployed_working_1)
        order_equipment_2 = OrderEquipment.objects.create(order=order, equipment=self.equipment_deployed_working_2)
        return order

    def create_order_collect_partial(self) -> Order:
        order = CollectOrder.objects.create(
            customer=self.customer_1,
            location=self.customer_1_location_1.location,
            date=timezone.now()
        )
        order_equipment_1 = OrderEquipment.objects.create(order=order, equipment=self.equipment_picked_up_working_1)
        order_equipment_2 = OrderEquipment.objects.create(order=order, equipment=self.equipment_deployed_working_2)
        order.perform_equipment_activity(team_lead=self.user, equipment=order_equipment_1.equipment)
        return order

    def create_order_collect_complete(self) -> Order:
        order = CollectOrder.objects.create(
            customer=self.customer_1,
            location=self.customer_1_location_1.location,
            date=timezone.now()
        )
        order_equipment_1 = OrderEquipment.objects.create(order=order, equipment=self.equipment_picked_up_working_1)
        order_equipment_2 = OrderEquipment.objects.create(order=order, equipment=self.equipment_picked_up_working_2)
        order.perform_equipment_activity(team_lead=self.user, equipment=order_equipment_1.equipment)
        order.perform_equipment_activity(team_lead=self.user, equipment=order_equipment_2.equipment)
        return order

    def create_order_deploy_initial(self) -> Order:
        order = DeployOrder.objects.create(
            customer=self.customer_1,
            location=self.customer_1_location_1.location,
            date=timezone.now(),
        )

        OrderGenericProduct.objects.create(
            order=order,
            generic_product=self.generic_product,
            quantity=2
        )
        return order

    def create_order_deploy_partial(self) -> Order:
        order = DeployOrder.objects.create(
            customer=self.customer_1,
            location=self.customer_1_location_1.location,
            date=timezone.now(),
        )
        OrderGenericProduct.objects.create(
            order=order,
            generic_product=self.generic_product,
            quantity=2
        )
        order_equipment_1 = OrderEquipment.objects.create(order=order, equipment=self.equipment_deployed_working_1)
        order.perform_equipment_activity(team_lead=self.user, equipment=order_equipment_1.equipment)
        return order

    def create_order_deploy_complete(self) -> Order:
        order = DeployOrder.objects.create(
            customer=self.customer_1,
            location=self.customer_1_location_1.location,
            date=timezone.now(),
        )
        OrderGenericProduct.objects.create(
            order=order,
            generic_product=self.generic_product,
            quantity=2
        )
        order_equipment_1 = OrderEquipment.objects.create(order=order, equipment=self.equipment_deployed_working_1)
        order_equipment_2 = OrderEquipment.objects.create(order=order, equipment=self.equipment_deployed_working_2)
        order.perform_equipment_activity(team_lead=self.user, equipment=order_equipment_1.equipment)
        order.perform_equipment_activity(team_lead=self.user, equipment=order_equipment_2.equipment)

        return order

    def create_order_inspect(self):
        order = InspectOrder.objects.create(
            customer=self.customer_1,
            location=self.customer_1_location_1.location,
            date=timezone.now())
        return order
