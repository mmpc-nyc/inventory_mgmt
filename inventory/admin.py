from django.contrib.admin import register
from simple_history.admin import SimpleHistoryAdmin

from inventory.models import InventoryItem, Location, Inventory, InventoryItemType


@register(InventoryItem)
class InventoryItemAdmin(SimpleHistoryAdmin):
    list_display = [
        'name',
        'label',
        'job',
        'status',
        'employee',
        'condition',
        'inventory',
        'inventoryitem_type',
    ]
    history_list_display = list_display


@register(InventoryItemType)
class InventoryItemTypeAdmin(SimpleHistoryAdmin):
    pass


@register(Inventory)
class InventoryAdmin(SimpleHistoryAdmin):
    pass

@register(Location)
class LocationAdmin(SimpleHistoryAdmin):
    pass