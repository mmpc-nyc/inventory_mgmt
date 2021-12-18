from django_filters import FilterSet, rest_framework as filters

from inventory.models import Product, Inventory, ProductType
from main.filters import User


class ProductFilter(FilterSet):

    name = filters.CharFilter(field_name='name', lookup_expr='contains')
    label = filters.CharFilter(field_name='label', lookup_expr='contains')
    status = filters.ChoiceFilter(choices= Product.ProductStatus.choices)
    inventory = filters.ModelChoiceFilter(queryset=Inventory.objects.all())
    product_type = filters.ModelChoiceFilter(queryset=ProductType.objects.all())
    employee = filters.ModelChoiceFilter(queryset=User.objects.all())
    editor = filters.ModelChoiceFilter(queryset=User.objects.all())
    edited = filters.DateTimeFilter()
    creator = filters.ModelChoiceFilter(queryset=User.objects.all())

    class Meta:
        model = Product
        fields = (
            'name',
            'label',
            'status',
            'inventory',
            'job',
            'product_type',
            'employee',
            'editor',
            'edited',
            'creator',
            'created',
        )