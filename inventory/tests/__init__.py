from django.contrib.auth import get_user_model
from django.test import TestCase

from common.models.contact import Contact
from customers.models.customer import Customer, ServiceLocation
from common.models.address import Address
from inventory.models.equipment import Equipment, Condition
from inventory.models.material import Material
from inventory.models.brand import Brand
from inventory.models.storage_location import StorageLocation

User = get_user_model()


class AbstractTest(TestCase):
    fixtures = ['fixtures/test.json', ]

    def setUp(self):
        self.user = User.objects.create(username='user', password='user')
        self.recipient = User.objects.create(username='recipient', password='recipient', )
        self.customer_email = "customer@email.com"
        self.customer_phone = "2122198218"
        self.customer_contact = Contact.objects.create(first_name="Customer", last_name="contact")
        self.location_storage_location = Address.objects.create(
            name='Storage Location 1',
            street_address='Storage Location 1',
            city="Storage Location City",
            state="Storage LocationState",
            postal_code="00000",
            latitude=0,
            longitude=0, )
        self.location_customer_1 = Address.objects.create(
            name='Customer Location 1',
            street_address='Customer Location 1',
            city="Customer City",
            state="Customer State",
            postal_code="00000",
            latitude=0,
            longitude=0,
        )
        self.location_customer_2 = Address.objects.create(
            name='Customer Location 2',
            street_address='Customer Location 2',
            city="Customer City",
            state="Customer State",
            postal_code="00000",
            latitude=0,
            longitude=0,
        )
        self.location_user = Address.objects.create(
            name='User Location 2',
            street_address='User Location 2',
            city="User City",
            state="User State",
            postal_code="00000",
            latitude=0,
            longitude=0, )
        self.storage_location = StorageLocation.objects.create(name='Storage Location1', location=self.location_storage_location)
        self.billing_location_1 = Address.objects.create(
            name='Billing Location 1',
            street_address='Billing Location 1',
            city="Billing City",
            state="Billing State",
            postal_code="00000",
            latitude=0,
            longitude=0
        )
        self.billing_location_2 = Address.objects.create(
            name='Billing Location 1',
            street_address='Billing Location 1',
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
        self.material = Material.objects.create(
            name='Material 1',
            brand=self.brand,
        )
        self.condition_working = Condition.objects.get(name='Working')
        self.condition_damaged = Condition.objects.get(name='Damaged')
        self.condition_decommissioned = Condition.objects.get(name='Decommissioned')
        self.equipment_stored_working = Equipment.objects.create(
            name='stored_working',
            material=self.material,
            condition=self.condition_working,
            storage_location=self.storage_location,
            location=self.storage_location.address
        )
        self.equipment_picked_up_working_1 = Equipment.objects.create(
            name='picked_up_working_1',
            material=self.material,
            condition=self.condition_working,
            storage_location=self.storage_location,
            location=self.location_user,
            user=self.user,
            status=Equipment.Status.PICKED_UP
        )
        self.equipment_picked_up_working_2 = Equipment.objects.create(
            name='picked_up_working_2',
            material=self.material,
            condition=self.condition_working,
            storage_location=self.storage_location,
            location=self.location_user,
            user=self.user,
            status=Equipment.Status.PICKED_UP
        )
        self.equipment_deployed_working_1 = Equipment.objects.create(
            name='deployed_working_1',
            material=self.material,
            condition=self.condition_working,
            storage_location=self.storage_location,
            status=Equipment.Status.DEPLOYED
        )
        self.equipment_deployed_working_2 = Equipment.objects.create(
            name='deployed_working_2',
            material=self.material,
            condition=self.condition_working,
            storage_location=self.storage_location,
            status=Equipment.Status.DEPLOYED
        )