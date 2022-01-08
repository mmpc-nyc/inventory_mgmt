from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.exceptions import exception_serializer
from api.serializers import BrandSerializer, EquipmentSerializer, ProductSerializer, CategorySerializer, \
    EmailSerializer, PhoneNumberSerializer, ContactSerializer, CustomerSerializer, LocationSerializer, \
    GenericProductSerializer, OrderSerializer, StockSerializer, ProductTypeSerializer, UserSerializer


class BrandViewSet(viewsets.ModelViewSet):
    serializer_class = BrandSerializer
    queryset = serializer_class.Meta.model.objects.all()


class LocationViewSet(viewsets.ModelViewSet):
    serializer_class = LocationSerializer
    queryset = serializer_class.Meta.model.objects.all()


class GenericProductViewSet(viewsets.ModelViewSet):
    serializer_class = GenericProductSerializer
    queryset = serializer_class.Meta.model.objects.all()


class EquipmentViewSet(viewsets.ModelViewSet):
    serializer_class = EquipmentSerializer
    queryset = serializer_class.Meta.model.objects.all()


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = serializer_class.Meta.model.objects.all()


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = serializer_class.Meta.model.objects.all()


class EmailViewSet(viewsets.ModelViewSet):
    serializer_class = EmailSerializer
    queryset = serializer_class.Meta.model.objects.all()


class PhoneNumberViewSet(viewsets.ModelViewSet):
    serializer_class = PhoneNumberSerializer
    queryset = serializer_class.Meta.model.objects.all()


class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    queryset = serializer_class.Meta.model.objects.all()


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = serializer_class.Meta.model.objects.all()


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = serializer_class.Meta.model.objects.all()

    @exception_serializer
    @action(detail=True, methods=['get'])
    def complete(self, request, pk):
        order = self.get_object()
        order.complete()
        return Response(self.serializer_class(order, many=False, context={'request': request}).data)


class StockViewSet(viewsets.ModelViewSet):
    serializer_class = StockSerializer
    queryset = serializer_class.Meta.model.objects.all()


class ProductTypeViewSet(viewsets.ModelViewSet):
    serializer_class = ProductTypeSerializer
    queryset = serializer_class.Meta.model.objects.all()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = serializer_class.Meta.model.objects.all()
