from django.contrib.admin import register
from simple_history.admin import SimpleHistoryAdmin

from inventory.models import Product, Location, Inventory, ProductType


@register(Product)
class ProductAdmin(SimpleHistoryAdmin):
    list_display = [
        'name',
        'label',
        'job',
        'status',
        'employee',
        'condition',
        'inventory',
        'product_type',
    ]
    history_list_display = list_display


@register(ProductType)
class ProductTypeAdmin(SimpleHistoryAdmin):
    pass


@register(Inventory)
class InventoryAdmin(SimpleHistoryAdmin):
    pass

@register(Location)
class LocationAdmin(SimpleHistoryAdmin):
    pass