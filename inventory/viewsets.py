from rest_framework import viewsets

from inventory.models import Brand
from inventory.serializers import BrandSerializer


class BrandViewSet(viewsets.ModelViewSet):
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()