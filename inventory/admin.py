from django.contrib.admin import register, ModelAdmin, TabularInline
from mptt.admin import MPTTModelAdmin

from inventory.models.customer import Customer, ServiceLocation
from inventory.models.equipment import Equipment, Condition
from inventory.models.material import Material, MaterialType, Brand, MaterialCategory
from inventory.models.material import MaterialField
from inventory.models.stock_location import StockLocation
from inventory.models.target import Target
from inventory.models.unit import Unit, UnitCategory
from inventory.models.vendor import Vendor


@register(ServiceLocation)
class CustomerLocationAdmin(ModelAdmin):
    list_display = ('customer', 'location')


@register(Customer)
class CustomerAdmin(MPTTModelAdmin):
    list_display = ('first_name', 'last_name', 'company_name', 'parent')


@register(Equipment)
class EquipmentAdmin(ModelAdmin):
    list_display = ('id', 'name', 'status', 'condition', 'stock_location', 'location', 'user',)


@register(StockLocation)
class StockLocationAdmin(ModelAdmin):
    list_display = ('name', 'status', 'location',)


@register(MaterialCategory)
class MaterialCategoryAdmin(MPTTModelAdmin):
    ...


@register(MaterialType)
class MaterialTypeAdmin(ModelAdmin):
    list_display = ('name',)


@register(Brand)
class BrandAdmin(ModelAdmin):
    list_display = ('name',)


@register(Condition)
class ConditionAdmin(ModelAdmin):
    list_display = ['name', 'description']


class MaterialFieldInline(TabularInline):
    model = MaterialField


@register(Material)
class MaterialAdmin(ModelAdmin):
    list_display = ('name', 'brand')

    inlines = [
        MaterialFieldInline,
    ]
    history_list_display = list_display


@register(Vendor)
class VendorAdmin(ModelAdmin):
    ...


@register(Unit)
class UnitAdmin(ModelAdmin):
    list_display = ['name', 'abbreviation', 'conversion_factor', 'is_metric']


@register(UnitCategory)
class UnitCategoryAdmin(ModelAdmin):
    pass


@register(Target)
class TargetAdmin(ModelAdmin):
    list_display = ['name', 'description', 'parent', ]
