from django.contrib.auth import get_user_model
from django_filters import FilterSet, rest_framework as filters

from inventory.models.material import Material
from inventory.models.stock_location import StockLocation

User = get_user_model()


class MaterialFilter(FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='contains')
    status = filters.ChoiceFilter(choices=Material.Status.choices)
    warehouse = filters.ModelChoiceFilter(queryset=StockLocation.objects.all())
    user = filters.ModelChoiceFilter(queryset=User.objects.all())

    class Meta:
        model = Material
        fields = ('name', 'status',)
