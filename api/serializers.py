from django.contrib.auth import get_user_model
from rest_framework import serializers

from inventory.models import Contact, Email, PhoneNumber, Location, Customer, CustomerLocation, CustomerContact, \
    Equipment, Condition, GenericProduct, Category, Product, ProductType, Brand, Stock
from inventory.models import Order

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'first_name', 'last_name', 'email', ]


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'url', 'name']


class PhoneNumberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ['id', 'url', 'phone_number']


class EmailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Email
        fields = ['id', 'url', 'email']


class ContactSerializer(serializers.HyperlinkedModelSerializer):
    emails = EmailSerializer(many=True, read_only=True)
    phone_numbers = PhoneNumberSerializer(many=True, read_only=True)

    class Meta:
        model = Contact
        fields = ['id', 'url', 'first_name', 'last_name', 'emails', 'phone_numbers']


class CustomerLocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomerLocation
        fields = ['customer', 'location', ]


class CustomerContactSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomerContact
        fields = ['customer', 'contact']


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    contacts = ContactSerializer(many=True, read_only=True)
    locations = LocationSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'url', 'first_name', 'last_name', 'company_name', 'parent', 'contacts', 'locations']


class BrandSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'url', 'name']


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'parent']


class GenericProductSerializer(serializers.HyperlinkedModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = GenericProduct
        fields = ['id', 'url', 'name', 'category', 'status']


class ProductTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductType
        fields = ['id', 'url', 'name']


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    brand = BrandSerializer()
    generic_product = GenericProductSerializer()
    product_type = ProductTypeSerializer()

    class Meta:
        model = Product
        fields = ['id', 'url', 'name', 'brand', 'generic_product', 'status', 'product_type', ]


class StockSerializer(serializers.HyperlinkedModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = Stock
        fields = ['id', 'url', 'name', 'status', 'location']


class ConditionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Condition
        fields = ['name', 'description', 'is_deployable', 'is_storable']


class EquipmentSerializer(serializers.HyperlinkedModelSerializer):
    product = ProductSerializer()
    stock = StockSerializer()
    condition = ConditionSerializer(many=False)

    class Meta:
        model = Equipment
        fields = ['id', 'url', 'name', 'product', 'status', 'condition', 'stock', 'user', ]


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    location = LocationSerializer(read_only=True)
    customer = CustomerSerializer(read_only=True)
    equipments = EquipmentSerializer(many=True)
    generic_products = GenericProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'url', 'status', 'customer', 'location', 'date', 'equipments', 'generic_products']
