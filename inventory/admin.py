from django.contrib.admin import register, ModelAdmin, TabularInline
from django.contrib.contenttypes.admin import GenericStackedInline
from django.db import models
from django.db.models import Count
from django.forms import TextInput, Textarea
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from mptt.admin import MPTTModelAdmin

from common.models.field import Field
from inventory.models import Transfer, TransferAcceptance, Vehicle, VehicleEquipmentItem, VehicleMaterial
from inventory.models.brand import Brand
from inventory.models.equipment import Equipment, Condition, EquipmentCategory, EquipmentField, EquipmentClass, \
    EquipmentItem
from inventory.models.material import Material, MaterialClass, MaterialCategory, MaterialClassMembership
from inventory.models.material import MaterialField
from inventory.models.stock_location import StockLocation, MaterialStock
from inventory.models.transfer import TransferItem, TransferItemAcceptance
from inventory.models.vendor import Vendor


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


class MaterialStockInline(TabularInline):
    model = MaterialStock
    extra = 1


class EquipmentItemInline(TabularInline):
    model = EquipmentItem
    extra = 1

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'purchased_by':
            kwargs['initial'] = request.user.id
            return db_field.formfield(**kwargs)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@register(Equipment)
class EquipmentAdmin(ModelAdmin):
    list_display = (
        'name', 'brand', 'category', 'equipment_class', 'asset_type', 'warranty_days', 'equipmentitem_count')
    list_filter = ('brand', 'category', 'equipment_class')
    inlines = (EquipmentItemInline, EquipmentFieldInline)
    search_fields = ('name',)
    ordering = ('name',)

    fieldsets = (
        (None, {'fields': ('name', 'brand', 'asset_type')}),
        ('Additional Information', {'fields': ('category', 'equipment_class', 'warranty_days')}),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('category', 'equipment_class', 'brand')
        queryset = queryset.annotate(equipmentitem_count=Count('equipmentitem'))
        return queryset

    def equipmentitem_count(self, obj):
        count = obj.equipmentitem_count
        url = reverse('admin:inventory_equipmentitem_changelist') + f'?equipment__id__exact={obj.id}'
        return format_html('<a href="{}">{}</a>', url, count)

    equipmentitem_count.admin_order_field = 'equipmentitem_count'
    equipmentitem_count.short_description = 'Equipment Items'


@register(EquipmentItem)
class EquipmentItemAdmin(ModelAdmin):
    list_display = (
        'equipment', 'serial_number', 'condition', 'purchase_price', 'purchased_by', 'purchase_date', 'status',
        'stock_location', 'warranty_expiration_date'
    )
    list_filter = ('equipment', 'status', 'condition', 'stock_location')
    search_fields = ('equipment__name', 'serial_number', 'notes', 'condition__name', 'stock_location__name')
    fieldsets = (
        (None, {
            'fields': ('equipment', 'serial_number', 'condition', 'status')
        }),
        ('Details', {
            'fields': ('purchase_price', 'purchased_by', 'purchase_date', 'notes', 'warranty_expiration_date')
        }),
        ('Stock Location', {
            'fields': ('stock_location',)
        })
    )

    def get_changeform_initial_data(self, request):
        initial_data = super().get_changeform_initial_data(request)
        initial_data['purchased_by'] = request.user.pk
        return initial_data

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('equipment', 'serial_number', 'condition', 'warranty_expiration_date',)
        else:
            return self.readonly_fields


@register(EquipmentField)
class EquipmentFieldAdmin(ModelAdmin):
    ...


@register(EquipmentClass)
class EquipmentClassAdmin(ModelAdmin):
    ...


@register(StockLocation)
class StockLocationAdmin(ModelAdmin):
    list_display = ('name', 'address', 'status')
    search_fields = ('name', 'location__street_address', 'location__city', 'location__state')
    list_filter = ('status',)
    actions = ['deactivate_stock_location']

    def deactivate_stock_location(self, request, queryset):
        queryset.update(status=StockLocation.StockLocationStatus.INACTIVE)

    deactivate_stock_location.short_description = 'Deactivate selected stock locations'


@register(Brand)
class BrandAdmin(ModelAdmin):
    list_display = ('name',)


@register(Condition)
class ConditionAdmin(ModelAdmin):
    list_display = ['name', 'description']


@register(Material)
class MaterialAdmin(ModelAdmin):
    list_display = ('name', 'get_targets', 'brand', 'category', 'is_taxable', 'is_active')
    list_filter = ('brand', 'category', 'is_taxable', 'is_active')
    search_fields = ('name', 'description')
    filter_horizontal = ('material_classes', 'targets')

    inlines = [
        MaterialFieldInline,
    ]
    history_list_display = list_display

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'brand', 'category', 'targets')
        }),
        ('Pricing', {
            'fields': (
                'is_taxable', 'is_active', 'is_product', 'product_sell_price', 'material_sell_price',
                'preferred_vendor')
        }),
        ('Units', {
            'fields': ('usage_unit', 'retail_unit')
        }),
    )

    def get_targets(self, obj):
        return ", ".join([t.name for t in obj.targets.all()])

    get_targets.short_description = 'Targets'


@register(Vendor)
class VendorAdmin(ModelAdmin):
    ...


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


class TransferItemInline(TabularInline):
    model = TransferItem
    min_num = 1


@register(Transfer)
class TransferAdmin(ModelAdmin):
    list_display = ('created_at', 'source', 'destination', 'agent', 'status')
    search_fields = ('item__name', 'source__name', 'destination__name')
    list_filter = ('status',)
    inlines = (TransferItemInline,)


class TransferItemAcceptanceInline(TabularInline):
    model = TransferItemAcceptance
    extra = 1


@register(TransferAcceptance)
class TransferAcceptanceAdmin(ModelAdmin):
    list_display = ('transfer', 'accepted_by', 'accepted_at')
    search_fields = (
        'transfer__item__name', 'transfer__source__name', 'transfer__destination__name', 'accepted_by__first_name',
        'accepted_by__last_name')
    list_filter = ('transfer__status', 'accepted_at')
    inlines = (TransferItemAcceptanceInline,)


class VehicleMaterialInline(TabularInline):
    model = VehicleMaterial
    extra = 1


class VehicleEquipmentItemInline(TabularInline):
    model = VehicleEquipmentItem
    extra = 1


@register(Vehicle)
class VehicleAdmin(ModelAdmin):
    inlines = [VehicleMaterialInline, VehicleEquipmentItemInline]
    list_display = ['name', 'vehicle_type', 'driver', 'vin_number', 'license_plate', 'make', 'model', 'model_year']
    list_filter = ('vehicle_type', 'make', 'model_year')
    search_fields = ['name', 'driver', 'vin_number', 'license_plate', 'make', 'model', 'model_year']
    fieldsets = (
        (None, {
            'fields': ('name', 'vehicle_type', 'driver')
        }),
        ('Vehicle Details', {
            'fields': ('vin_number', 'license_plate', 'make', 'model', 'model_year')
        }),
    )
