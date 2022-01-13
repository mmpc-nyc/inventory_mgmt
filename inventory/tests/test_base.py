from django.contrib.auth import get_user_model
from django.test import TestCase

from inventory.models import Location, Stock, Customer, CustomerLocation, Brand, ProductType, GenericProduct, Product, \
    Condition, Equipment, Order

User = get_user_model()


class AbstractTest(TestCase):
    fixtures = ['fixtures/db.json', ]

    def setUp(self):
        self.user = User.objects.create(username='user', password='user')
        self.recipient = User.objects.create(username='recipient', password='recipient', )
        self.location_stock = Location.objects.create(raw='Stock Location')
        self.location_customer = Location.objects.create(raw='Customer Location')
        self.location_user = Location.objects.create(raw='User Location')
        self.stock = Stock.objects.create(name='Stock 1', location=self.location_stock)
        self.customer = Customer.objects.create(first_name='Test', last_name='Customer')
        self.customer_location = CustomerLocation.objects.create(customer=self.customer,
                                                                 location=self.location_customer)
        self.brand = Brand.objects.create(name='Brand 1')
        self.product_type_equipment = ProductType.objects.create(name='Equipment')
        self.generic_product = GenericProduct.objects.create(name='Generic Product 1')
        self.product = Product.objects.create(name='Product 1', generic_product=self.generic_product, brand=self.brand,
                                              product_type=self.product_type_equipment)
        self.condition_working = Condition.objects.get(name='Working')
        self.condition_damaged = Condition.objects.get(name='Damaged')
        self.condition_decommissioned = Condition.objects.get(name='Decommissioned')
        self.equipment_stored_working = Equipment.objects.create(name='stored_working', product=self.product,
            condition=self.condition_working, stock=self.stock, location=self.stock.location

        )
        self.equipment_picked_up_working = Equipment.objects.create(name='picked_up_working', product=self.product,
            condition=self.condition_working, stock=self.stock, location=self.location_user, user=self.user,
            status=Equipment.Status.PICKED_UP)
        self.order = Order.objects.get(id=1)
