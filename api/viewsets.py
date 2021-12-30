from rest_framework import viewsets

from inventory.models.product import Brand
from api.serializers import BrandSerializer


class BrandViewSet(viewsets.ModelViewSet):
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()