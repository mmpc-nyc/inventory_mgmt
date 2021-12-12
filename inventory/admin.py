from django.contrib.admin import register
from simple_history.admin import SimpleHistoryAdmin

from inventory.models.inventory_models import Item, ItemType, Storage


@register(Item)
class ItemAdmin(SimpleHistoryAdmin):
    list_display = [
        'name',
        'label',
        'job',
        'status',
        'employee',
        'condition',
        'storage',
        'item_type',
    ]
    history_list_display = list_display


@register(ItemType)
class ItemTypeAdmin(SimpleHistoryAdmin):
    pass


@register(Storage)
class InventoryAdmin(SimpleHistoryAdmin):
    pass