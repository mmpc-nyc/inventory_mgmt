from django.contrib.auth import get_user_model
from django_filters import FilterSet, rest_framework as filters

from inventory.models.product import Product
from inventory.models.stock_location import StockLocation

User = get_user_model()


class ProductFilter(FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='contains')
    status = filters.ChoiceFilter(choices=Product.Status.choices)
    warehouse = filters.ModelChoiceFilter(queryset=StockLocation.objects.all())
    user = filters.ModelChoiceFilter(queryset=User.objects.all())

    class Meta:
        model = Product
        fields = ('name', 'status',)
