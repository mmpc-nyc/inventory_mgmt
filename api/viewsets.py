import rest_framework.permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from api.serializers import BrandSerializer, EquipmentSerializer, MaterialSerializer, MaterialCategorySerializer, \
    EmailSerializer, PhoneNumberSerializer, ContactSerializer, CustomerSerializer, LocationSerializer, \
    StockLocationSerializer, MaterialTypeSerializer, UserSerializer
from inventory.models.equipment import Equipment


class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = [rest_framework.permissions.IsAuthenticated, ]


class BrandViewSet(BaseViewSet):
    serializer_class = BrandSerializer
    queryset = serializer_class.Meta.model.objects.all()


class LocationViewSet(BaseViewSet):
    serializer_class = LocationSerializer
    queryset = serializer_class.Meta.model.objects.all()


class EquipmentViewSet(BaseViewSet):
    serializer_class = EquipmentSerializer
    queryset = Equipment.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name']


class MaterialViewSet(BaseViewSet):
    serializer_class = MaterialSerializer
    queryset = serializer_class.Meta.model.objects.all()


class MaterialCategoryViewSet(BaseViewSet):
    serializer_class = MaterialCategorySerializer
    queryset = serializer_class.Meta.model.objects.all()


class EmailViewSet(BaseViewSet):
    serializer_class = EmailSerializer
    queryset = serializer_class.Meta.model.objects.all()


class PhoneNumberViewSet(BaseViewSet):
    serializer_class = PhoneNumberSerializer
    queryset = serializer_class.Meta.model.objects.all()


class ContactViewSet(BaseViewSet):
    serializer_class = ContactSerializer
    queryset = serializer_class.Meta.model.objects.all()


class CustomerViewSet(BaseViewSet):
    serializer_class = CustomerSerializer
    queryset = serializer_class.Meta.model.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['first_name', 'last_name', 'company_name', 'email', 'phone_number']
    search_fields = ['first_name', 'last_name', 'company_name', 'email', 'phone_number']


class StockLocationViewSet(BaseViewSet):
    serializer_class = StockLocationSerializer
    queryset = serializer_class.Meta.model.objects.all()


class MaterialTypeViewSet(BaseViewSet):
    serializer_class = MaterialTypeSerializer
    queryset = serializer_class.Meta.model.objects.all()


class UserViewSet(BaseViewSet):
    serializer_class = UserSerializer
    queryset = serializer_class.Meta.model.objects.all()
