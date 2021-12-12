from django_filters import FilterSet, rest_framework as filters

from inventory.models import Item, Storage, ItemType
from main.filters import User


class ItemFilter(FilterSet):

    name = filters.CharFilter(field_name='name', lookup_expr='contains')
    label = filters.CharFilter(field_name='label', lookup_expr='contains')
    status = filters.ChoiceFilter(choices= Item.ItemStatus.choices)
    storage = filters.ModelChoiceFilter(queryset=Storage.objects.all())
    item_type = filters.ModelChoiceFilter(queryset=ItemType.objects.all())
    employee = filters.ModelChoiceFilter(queryset=User.objects.all())
    editor = filters.ModelChoiceFilter(queryset=User.objects.all())
    edited = filters.DateTimeFilter()
    creator = filters.ModelChoiceFilter(queryset=User.objects.all())

    class Meta:
        model = Item
        fields = (
            'name',
            'label',
            'status',
            'storage',
            'job',
            'item_type',
            'employee',
            'editor',
            'edited',
            'creator',
            'created',
        )