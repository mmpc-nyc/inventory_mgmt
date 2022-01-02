from rest_framework import serializers
from django.contrib.auth import get_user_model
from inventory.models import Equipment, GenericProduct, Category, Contact, Customer, Location, Email, Order, Stock
from inventory.models.product import Brand, Product, ProductType

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
        model = Location
        fields = ['id', 'url', 'phone_number']


class EmailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Email
        fields = ['id', 'url', 'email']


class ContactSerializer(serializers.HyperlinkedModelSerializer):
    emails = EmailSerializer(many=True, )
    phone_numbers = PhoneNumberSerializer(many=True, )

    class Meta:
        model = Contact
        fields = ['id', 'url', 'first_name', 'last_name', 'emails', 'phone_numbers']


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    contacts = ContactSerializer(many=True, )
    locations = LocationSerializer(many=True, )

    class Meta:
        model = Customer
        fields = ['id', 'url', 'first_name', 'last_name', 'company_name', 'contacts', 'parent', 'locations']


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


class EquipmentSerializer(serializers.HyperlinkedModelSerializer):
    product = ProductSerializer()
    stock = StockSerializer()

    class Meta:
        model = Equipment
        fields = ['id', 'url', 'name', 'product', 'status', 'condition', 'stock', 'employee', ]


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    customer = CustomerSerializer()
    location = LocationSerializer()

    class Meta:
        model = Order
        fields = ['id', 'url', 'customer', 'status', 'location', 'date']
