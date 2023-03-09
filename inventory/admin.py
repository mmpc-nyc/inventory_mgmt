from django.contrib.admin import register, ModelAdmin, TabularInline
from mptt.admin import MPTTModelAdmin

from inventory.models.contact import Contact, ContactPhoneNumber, ContactEmail, PhoneNumber
from inventory.models.customer import Customer, ServiceLocation
from inventory.models.equipment import Equipment, Condition
from inventory.models.field import Field
from inventory.models.location import Location
from inventory.models.material import Material, MaterialType, Brand, MaterialCategory
from inventory.models.material import MaterialField
from inventory.models.stock_location import StockLocation
from inventory.models.target import Target
from inventory.models.unit import Unit, UnitCategory
from inventory.models.vendor import Vendor


@register(ServiceLocation)
class CustomerLocationAdmin(ModelAdmin):
    list_display = ('customer', 'location')


@register(ContactEmail)
class ContactEmailAdmin(ModelAdmin):
    list_display = ('contact', 'email',)


@register(ContactPhoneNumber)
class ContactPhoneNumberAdmin(ModelAdmin):
    list_display = ('contact', 'phone_number',)


@register(Customer)
class CustomerAdmin(MPTTModelAdmin):
    list_display = ('first_name', 'last_name', 'company_name', 'parent')


@register(Contact)
class ContactAdmin(ModelAdmin):
    list_display = ('first_name', 'last_name',)


@register(Equipment)
class EquipmentAdmin(ModelAdmin):
    list_display = ('id', 'name', 'status', 'condition', 'warehouse', 'location', 'user',)


@register(StockLocation)
class StockLocationAdmin(ModelAdmin):
    list_display = ('name', 'status', 'location',)


@register(MaterialCategory)
class CategoryAdmin(MPTTModelAdmin):
    ...


@register(MaterialType)
class MaterialTypeAdmin(ModelAdmin):
    list_display = ('name',)


@register(Brand)
class BrandAdmin(ModelAdmin):
    list_display = ('name',)


@register(Location)
class LocationAdmin(ModelAdmin):
    ...


@register(PhoneNumber)
class PhoneNumberAdmin(ModelAdmin):
    ...


@register(Condition)
class ConditionAdmin(ModelAdmin):
    list_display = ['name', 'description']


@register(Field)
class FieldAdmin(ModelAdmin):
    list_display = ['name', 'content_type', 'field_type', 'validation_type', 'default_value', 'is_required']


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
