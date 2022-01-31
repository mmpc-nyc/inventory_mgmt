import rest_framework.permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from api.exceptions import exception_serializer
from api.serializers import BrandSerializer, EquipmentSerializer, ProductSerializer, CategorySerializer, \
    EmailSerializer, PhoneNumberSerializer, ContactSerializer, CustomerSerializer, LocationSerializer, \
    GenericProductSerializer, OrderSerializer, WarehouseSerializer, ProductTypeSerializer, UserSerializer


class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = [rest_framework.permissions.IsAuthenticated,]


class BrandViewSet(BaseViewSet):
    serializer_class = BrandSerializer
    queryset = serializer_class.Meta.model.objects.all()


class LocationViewSet(BaseViewSet):
    serializer_class = LocationSerializer
    queryset = serializer_class.Meta.model.objects.all()


class GenericProductViewSet(BaseViewSet):
    serializer_class = GenericProductSerializer
    queryset = serializer_class.Meta.model.objects.all()


class EquipmentViewSet(BaseViewSet):
    serializer_class = EquipmentSerializer
    queryset = serializer_class.Meta.model.objects.all()


class ProductViewSet(BaseViewSet):
    serializer_class = ProductSerializer
    queryset = serializer_class.Meta.model.objects.all()


class CategoryViewSet(BaseViewSet):
    serializer_class = CategorySerializer
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
    filterset_fields= ['first_name', 'last_name', 'company_name', 'email', 'phone_number']
    search_fields = ['first_name', 'last_name', 'company_name', 'email', 'phone_number']


class OrderViewSet(BaseViewSet):
    serializer_class = OrderSerializer
    queryset = serializer_class.Meta.model.objects.all()

    @exception_serializer
    @action(detail=True, methods=['get'])
    def complete(self, request, pk):
        order = self.get_object()
        order.complete()
        return Response(self.serializer_class(order, many=False, context={'request': request}).data)


class WarehouseViewSet(BaseViewSet):
    serializer_class = WarehouseSerializer
    queryset = serializer_class.Meta.model.objects.all()


class ProductTypeViewSet(BaseViewSet):
    serializer_class = ProductTypeSerializer
    queryset = serializer_class.Meta.model.objects.all()


class UserViewSet(BaseViewSet):
    serializer_class = UserSerializer
    queryset = serializer_class.Meta.model.objects.all()
