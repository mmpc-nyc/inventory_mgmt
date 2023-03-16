from django.contrib.admin import register, ModelAdmin, TabularInline, StackedInline
from django.contrib.contenttypes.admin import GenericStackedInline
from django.db import models
from django.forms import TextInput, Textarea
from django.utils.translation import gettext_lazy as _
from mptt.admin import MPTTModelAdmin

from common.models.field import Field
from inventory.models.brand import Brand
from inventory.models.customer import Customer, ServiceLocation
from inventory.models.equipment import Equipment, Condition, EquipmentCategory, EquipmentField, EquipmentClass
from inventory.models.material import Material, MaterialClass, MaterialCategory, MaterialClassMembership
from inventory.models.material import MaterialField
from inventory.models.service import Service, RequiredServiceMaterial, SuggestedServiceMaterial, ServiceProduct, \
    ServiceMaterialClass
from inventory.models.stock_location import StockLocation
from inventory.models.target import Target
from inventory.models.unit import Unit, UnitCategory
from inventory.models.vendor import Vendor
from inventory.models.warranty import Warranty, WarrantyTemplate


class RequiredServiceMaterialInline(TabularInline):
    model = RequiredServiceMaterial
    extra = 1


class SuggestedServiceMaterialInline(TabularInline):
    model = SuggestedServiceMaterial
    extra = 1


class ServiceProductInline(TabularInline):
    model = ServiceProduct
    extra = 1


class ServiceMaterialClassInline(TabularInline):
    model = ServiceMaterialClass
    extra = 1


class MaterialClassInline(TabularInline):
    model = MaterialClass
    extra = 1


class GenericFieldInline(GenericStackedInline):
    model = Field
    extra = 0


class EquipmentFieldInline(TabularInline):
    model = EquipmentField
    extra = 0


class MaterialFieldInline(TabularInline):
    model = MaterialField
    extra = 0


class MaterialClassMembershipInline(TabularInline):
    model = MaterialClassMembership
    extra = 1


class MaterialInline(TabularInline):
    model = Material
    extra = 1
    classes = ('collapse',)
    fieldsets = (
        (_('Material Information'), {
            'fields': ('name', 'description', 'brand', 'active', 'category',
                       'targets', 'is_taxable', 'is_active', 'is_product')
        }),
        (_('Pricing Information'), {
            'fields': ('product_sell_price', 'material_sell_price')
        }),
        (_('Inventory Information'), {
            'fields': ('preferred_vendor', 'usage_unit', 'retail_unit', 'min_stock', 'max_stock')
        })
    )
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '30'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 40})},
    }


@register(ServiceLocation)
class CustomerLocationAdmin(ModelAdmin):
    list_display = ('customer', 'location')


@register(Customer)
class CustomerAdmin(MPTTModelAdmin):
    list_display = ('first_name', 'last_name', 'company_name', 'parent')


@register(Equipment)
class EquipmentAdmin(ModelAdmin):
    list_display = ('id', 'name', 'status', 'condition', 'user',)

    inlines = [
        EquipmentFieldInline,
    ]


@register(EquipmentField)
class EquipmentFieldAdmin(ModelAdmin):
    ...


@register(EquipmentClass)
class EquipmentClassAdmin(ModelAdmin):
    ...


@register(StockLocation)
class StockLocationAdmin(ModelAdmin):
    list_display = ('name', 'status', 'location',)


@register(Brand)
class BrandAdmin(ModelAdmin):
    list_display = ('name',)


@register(Condition)
class ConditionAdmin(ModelAdmin):
    list_display = ['name', 'description']


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
    ordering = 'parent', 'name'


@register(MaterialCategory)
class MaterialCategoryAdmin(MPTTModelAdmin):
    inlines = [GenericFieldInline]


@register(EquipmentCategory)
class EquipmentCategoryAdmin(ModelAdmin):
    inlines = [GenericFieldInline]


@register(MaterialClass)
class MaterialClassAdmin(ModelAdmin):
    list_display = ('name', 'description')
    inlines = [MaterialClassMembershipInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('materialclassmembership_set__material')
        return queryset


@register(MaterialClassMembership)
class MaterialClassMembershipAdmin(ModelAdmin):
    list_display = ('material', 'material_class', 'priority')
    list_filter = ('material_class',)
    search_fields = ('material__name', 'material__description', 'material__id')


@register(Service)
class ServiceAdmin(ModelAdmin):
    inlines = [RequiredServiceMaterialInline, SuggestedServiceMaterialInline, ServiceProductInline,
               ServiceMaterialClassInline]
    list_display = ('name', 'price', 'is_active')
    search_fields = ('name',)
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
    }


@register(RequiredServiceMaterial)
class RequiredServiceMaterialAdmin(ModelAdmin):
    list_display = ['service', 'material', 'quantity']
    search_fields = ['service__name', 'material__name']
    list_filter = ['service__name', 'material__name']


@register(SuggestedServiceMaterial)
class SuggestedServiceMaterialAdmin(ModelAdmin):
    list_display = ['service', 'material', 'quantity']
    search_fields = ['service__name', 'material__name']
    list_filter = ['service__name', 'material__name']


@register(ServiceProduct)
class ServiceProductAdmin(ModelAdmin):
    list_display = ['service', 'product', 'quantity']
    search_fields = ['service__name', 'product__name']
    list_filter = ['service__name', 'product__name']


@register(ServiceMaterialClass)
class ServiceMaterialClassAdmin(ModelAdmin):
    list_display = ['service', 'material_class']
    search_fields = ['service__name', 'material_class__name']
    list_filter = ['service__name', 'material_class__name']


class WarrantyInline(StackedInline):
    model = Warranty


@register(WarrantyTemplate)
class WarrantyTemplateAdmin(ModelAdmin):
    inlines = [WarrantyInline]


@register(Warranty)
class WarrantyAdmin(ModelAdmin):
    ...
