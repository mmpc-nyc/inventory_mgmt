from django_filters import FilterSet, rest_framework as filters

from inventory.models import InventoryItem, Inventory, InventoryItemType
from main.filters import User


class InventoryItemFilter(FilterSet):

    name = filters.CharFilter(field_name='name', lookup_expr='contains')
    label = filters.CharFilter(field_name='label', lookup_expr='contains')
    status = filters.ChoiceFilter(choices= InventoryItem.InventoryItemStatus.choices)
    inventory = filters.ModelChoiceFilter(queryset=Inventory.objects.all())
    inventoryitem_type = filters.ModelChoiceFilter(queryset=InventoryItemType.objects.all())
    employee = filters.ModelChoiceFilter(queryset=User.objects.all())
    editor = filters.ModelChoiceFilter(queryset=User.objects.all())
    edited = filters.DateTimeFilter()
    creator = filters.ModelChoiceFilter(queryset=User.objects.all())

    class Meta:
        model = InventoryItem
        fields = (
            'name',
            'label',
            'status',
            'inventory',
            'job',
            'inventoryitem_type',
            'employee',
            'editor',
            'edited',
            'creator',
            'created',
        )