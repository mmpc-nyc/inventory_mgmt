from django_filters import FilterSet, rest_framework as filters
from inventory.models.modelsimport Product, Stock
from django.contrib.auth import get_user_model

User = get_user_model()


class ProductFilter(FilterSet):

    name = filters.CharFilter(field_name='name', lookup_expr='contains')
    status = filters.ChoiceFilter(choices= Product.Status.choices)
    stock = filters.ModelChoiceFilter(queryset=Stock.objects.all())
    user = filters.ModelChoiceFilter(queryset=User.objects.all())

    class Meta:
        model = Product
        fields = (
            'name',
            'status',
        )