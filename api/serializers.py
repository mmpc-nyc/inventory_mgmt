from django.contrib.auth import get_user_model
from rest_framework import serializers

from common.models.contact import Contact
from customers.models.customer import Customer, ServiceLocation
from common.models.address import Address
from inventory.models.equipment import Equipment, Condition
from inventory.models.material import Material, MaterialClass, MaterialCategory
from inventory.models.brand import Brand
from inventory.models.stock_location import StockLocation

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'first_name', 'last_name', 'email', ]


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'url', 'name', 'address_line_1', 'address_line_2', 'city', 'state', 'latitude', 'longitude']


class ContactSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Contact
        fields = ['id', 'url', 'first_name', 'last_name', 'emails', 'phone_numbers']


class CustomerLocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ServiceLocation
        fields = ['customer', 'location', ]


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    service_locations = LocationSerializer(many=True)
    billing_location = LocationSerializer()

    @staticmethod
    def get_location_contacts(location, customer) -> list:
        """Helper method for retrieving location contacts.
        If contact same customer setting is set then it defaults to the first contact of the customer record"""
        contacts = []
        if 'contact_same_as_customer' in location:
            contact_same_as_customer = location.pop('contact_same_as_customer')
            if contact_same_as_customer:
                contacts = [
                    {
                        'first_name': customer.first_name,
                        'last_name': customer.last_name,
                        'emails': [customer.email],
                        'phone_numbers': [customer.phone_number],
                    }
                ]  # Uses the first customer contact
        return contacts

    def __init__(self, *args, **kwargs):
        if 'data' in kwargs and 'billing_location_same_as_service_location' in kwargs['data']:
            if kwargs['data']['billing_location_same_as_service_location']:
                kwargs['data']['billing_location'] = kwargs['data']['service_locations'][0]
        super(CustomerSerializer, self).__init__(*args, **kwargs)

    def create(self, validated_data) -> Customer:
        # TODO Implement the related serializers and fix email / phone contact information

        service_locations = validated_data.pop('service_locations') if 'service_locations' in validated_data else []
        billing_location = validated_data.pop('billing_location') if 'billing_location' in validated_data else None

        service_location_objects = []
        for service_location in service_locations:
            service_location_contacts = self.get_location_contacts(location=service_location, customer=validated_data)
            service_location_objects.append(Address.objects.create(**service_location))
            # TODO Replace this code: for service_location_contact in service_location_contacts:
            # TODO Replace this code:    LocationContact.objects.create(location=service_location_objects[-1], **service_location_contact)

        # Creates Billing Location Record
        if 'billing_location_same_as_service_location' in self.initial_data and self.initial_data[
            'billing_location_same_as_service_location']:
            billing_location = service_location_objects[0]
        else:
            billing_location_contacts = self.get_location_contacts(location=billing_location,
                                                                   customer=validated_data)
            location = Address.objects.create(**billing_location)
            # TODO Replace this code: for billing_location_contact in billing_location_contacts:
            # TODO Replace this code:    LocationContact.objects.create(location=location, **billing_location_contact)

        # Creates Customer Record
        customer = Customer.objects.create(billing_location=billing_location, **validated_data)

        # Creates Service Locations Record
        for service_location_object in service_location_objects:
            ServiceLocation.objects.create(location=service_location_object, customer=customer)

        return customer

    class Meta:
        model = Customer
        fields = ['id', 'url', 'first_name', 'last_name', 'company_name', 'customer_type', 'email', 'phone_number',
                  'parent',
                  'billing_location',
                  'service_locations']


class BrandSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'url', 'name']


class MaterialCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MaterialCategory
        fields = ['name', 'parent']


class MaterialTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MaterialClass
        fields = ['id', 'url', 'name']


class MaterialSerializer(serializers.HyperlinkedModelSerializer):
    brand = BrandSerializer()

    class Meta:
        model = Material
        fields = ['id', 'url', 'name', 'brand', 'status', ]


class StockLocationSerializer(serializers.HyperlinkedModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = StockLocation
        fields = ['id', 'url', 'name', 'status', 'location']


class ConditionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Condition
        fields = ['name', 'description', 'action_collect', 'action_decommission', 'action_deploy', 'action_store',
                  'action_transfer', 'action_withdraw']


class EquipmentSerializer(serializers.HyperlinkedModelSerializer):
    material = MaterialSerializer()
    stock_location = StockLocationSerializer()
    condition = ConditionSerializer(many=False)

    class Meta:
        model = Equipment
        fields = ['id', 'url', 'name', 'material', 'status', 'condition', 'stock_location', 'user', ]