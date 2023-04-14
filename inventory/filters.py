from django.contrib.auth import get_user_model
from django_filters import FilterSet, rest_framework as filters

from inventory.models.material import Material
from inventory.models.storage_location import StorageLocation

User = get_user_model()


class MaterialFilter(FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='contains')
    status = filters.ChoiceFilter(choices=Material.Status.choices)
    storage_location = filters.ModelChoiceFilter(queryset=StorageLocation.objects.all())
    user = filters.ModelChoiceFilter(queryset=User.objects.all())

    class Meta:
        model = Material
        fields = ('name', 'status',)
