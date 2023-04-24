from django.contrib.admin import register, ModelAdmin, TabularInline, StackedInline
from django.contrib.contenttypes.admin import GenericStackedInline
from django.db import models
from django.db.models import Count
from django.forms import TextInput, Textarea
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from mptt.admin import MPTTModelAdmin
from common.models.field import Field
from inventory.models import Transfer, TransferAcceptance, Vehicle, VehicleEquipmentItem, VehicleMaterial, \
    PurchaseOrderItem, PurchaseOrder
from inventory.models.brand import Brand
from inventory.models.equipment import Equipment, Condition, EquipmentCategory, EquipmentField, EquipmentClass, \
    EquipmentItem
from inventory.models.material import Material, MaterialClass, MaterialCategory
from inventory.models.material import MaterialField
from inventory.models.storage_location import StorageLocation, MaterialStock
from inventory.models.transfer import TransferMaterialItem, TransferEquipmentItem
from inventory.models.vendor import Vendor, VendorMaterial, VendorEquipment


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
        'storage_location', 'warranty_expiration_date'
    )
    list_filter = ('equipment', 'status', 'condition', 'storage_location')
    search_fields = ('equipment__name', 'serial_number', 'notes', 'condition__name', 'storage_location__name')
    fieldsets = (
        (None, {
            'fields': ('equipment', 'serial_number', 'condition', 'status')
        }),
        ('Details', {
            'fields': ('purchase_price', 'purchased_by', 'purchase_date', 'notes', 'warranty_expiration_date')
        }),
        ('Storage Location', {
            'fields': ('storage_location',)
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


@register(StorageLocation)
class StorageLocationAdmin(ModelAdmin):
    list_display = ('name', 'address')
    fieldsets = (
        (None, {
            'fields': ('is_active', 'name', 'address', 'description',)
        }),
        ('Access Times', {
            'fields': (('access_monday_start', 'access_monday_end'),
                       ('access_tuesday_start', 'access_tuesday_end'),
                       ('access_wednesday_start', 'access_wednesday_end'),
                       ('access_thursday_start', 'access_thursday_end'),
                       ('access_friday_start', 'access_friday_end'),
                       ('access_saturday_start', 'access_saturday_end'),
                       ('access_sunday_start', 'access_sunday_end'))
        }),
    )


@register(Brand)
class BrandAdmin(ModelAdmin):
    list_display = ('name',)


@register(Condition)
class ConditionAdmin(ModelAdmin):
    list_display = ['name', 'description']


@register(Material)
class MaterialAdmin(ModelAdmin):
    list_display = (
        'name', 'get_targets', 'brand', 'category', 'material_class', 'material_sell_price', 'product_sell_price',
        'is_product', 'is_taxable', 'is_active')
    list_filter = ('brand', 'category', 'is_taxable', 'is_active')
    search_fields = ('name', 'description')
    filter_horizontal = ('targets',)
    readonly_fields = ('documentation_link',)

    inlines = [
        MaterialFieldInline,
    ]
    history_list_display = list_display

    fieldsets = (
        (None, {
            'fields': ('name', 'documentation', 'description', 'brand', 'category', 'material_class')
        }),
        ('Units', {
            'fields': ('usage_unit', 'retail_unit')
        }),
        ('Pricing', {
            'fields': (
                'is_taxable', 'is_active', 'is_product', 'product_sell_price', 'material_sell_price',
                'preferred_vendor')
        }),
        ('Targets', {
            'fields': ('targets',)
        })
    )

    def get_targets(self, obj):
        targets = obj.targets.all()
        links = []
        for target in targets:
            url = reverse('admin:common_target_change', args=[target.pk])
            link = f'<a href="{url}">{target.name}</a>'
            links.append(link)
        return format_html(', '.join(links))

    get_targets.short_description = 'Targets'

    def documentation_link(self, obj):
        if obj.documentation:
            return format_html('<a href="{0}" target="_blank">PDF</a>',
                               obj.documentation.url)
        else:
            return '-'

    documentation_link.short_description = 'Documentation'


class VendorMaterialInline(TabularInline):
    model = VendorMaterial
    extra = 0
    autocomplete_fields = ('material',)
    readonly_fields = ['current_price']

    def current_price(self, obj):
        return obj.current_price()

    current_price.short_description = 'Current Price'


class VendorEquipmentInline(TabularInline):
    model = VendorEquipment
    extra = 0
    autocomplete_fields = ('equipment',)
    readonly_fields = ['current_price']

    def current_price(self, obj):
        return obj.current_price()

    current_price.short_description = 'Current Price'


@register(Vendor)
class VendorAdmin(ModelAdmin):
    inlines = [VendorMaterialInline, VendorEquipmentInline]
    list_display = ('name', 'delivery_time', 'website_link', 'is_active')
    search_fields = ('name', 'website')
    list_filter = ('is_active',)
    fieldsets = (
        (None, {
            'fields': ('name', 'is_active')
        }),
        (_('Contact Information'), {
            'fields': ('delivery_time', 'website', 'contact')
        })
    )

    def website_link(self, obj):
        if obj.website:
            return format_html('<a href="{0}" target="_blank">{0}</a>', obj.website)
        else:
            return '-'

    website_link.short_description = _('Website')
    website_link.allow_tags = True


@register(VendorMaterial)
class VendorMaterialAdmin(ModelAdmin):
    list_display = ['material', 'sku', 'unit_price', 'promo_unit_price', 'promo_start_date', 'promo_end_date',
                    'current_price']
    list_display_links = ['material']
    list_filter = ['promo_start_date', 'promo_end_date']
    search_fields = ['material__name', 'sku']
    autocomplete_fields = ['material']


@register(VendorEquipment)
class VendorEquipmentAdmin(ModelAdmin):
    list_display = ['equipment', 'sku', 'unit_price', 'promo_unit_price', 'promo_start_date', 'promo_end_date',
                    'current_price']
    list_display_links = ['equipment']
    list_filter = ['promo_start_date', 'promo_end_date']
    search_fields = ['material__name', 'sku']
    autocomplete_fields = ['equipment']


@register(MaterialCategory)
class MaterialCategoryAdmin(MPTTModelAdmin):
    inlines = [GenericFieldInline]


@register(EquipmentCategory)
class EquipmentCategoryAdmin(ModelAdmin):
    inlines = [GenericFieldInline]


@register(MaterialClass)
class MaterialClassAdmin(ModelAdmin):
    list_display = ('name', 'description')


class TransferEquipmentItemInline(StackedInline):
    model = TransferEquipmentItem
    extra = 0


class TransferMaterialItemInline(StackedInline):
    model = TransferMaterialItem
    extra = 0


@register(Transfer)
class TransferAdmin(ModelAdmin):
    list_display = ('created_at', 'source', 'destination', 'agent', 'status')
    search_fields = ('item__name', 'source__name', 'destination__name')
    list_filter = ('status',)
    inlines = (TransferEquipmentItemInline, TransferMaterialItemInline)


@register(TransferAcceptance)
class TransferAcceptanceAdmin(ModelAdmin):
    list_display = ('transfer', 'accepted_by', 'accepted_at')
    search_fields = (
        'transfer__item__name', 'transfer__source__name', 'transfer__destination__name', 'accepted_by__first_name',
        'accepted_by__last_name')
    list_filter = ('transfer__status', 'accepted_at')


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


class PurchaseOrderItemInline(TabularInline):
    extra = 1
    readonly_fields = ('price', 'current_price')
    autocomplete_fields = ('vendor_material', 'vendor_equipment')

    def price(self, obj):
        return obj.quantity * obj.vendor_price

    price.short_description = _('Price')


@register(PurchaseOrder)
class PurchaseOrderAdmin(ModelAdmin):
    list_display = (
    'id', 'vendor', 'status', 'created_by', 'created_at', 'approved_by', 'approved_at', 'get_total_price')
    list_filter = ('status', 'created_by', 'approved_by')
    search_fields = ('id', 'vendor__name', 'created_by__username', 'approved_by__username')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_by', 'created_at', 'approved_by', 'approved_at', 'get_total_price')
    inlines = (PurchaseOrderItemInline,)
    autocomplete_fields = ('vendor',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def get_total_price(self, obj):
        return sum(item.price() for item in obj.items.all())

    get_total_price.short_description = _('Total Price')

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def response_change(self, request, obj):
        if '_approve' in request.POST:
            obj.status = PurchaseOrder.Status.INTERNALLY_APPROVED
            obj.approved_by = request.user
            obj.approved_at = timezone.now()
            obj.save()
            self.message_user(request, _('The purchase order has been approved.'))
            return self.response_post_save_change(request, obj)
        elif '_reject' in request.POST:
            obj.status = PurchaseOrder.Status.INTERNALLY_REJECTED
            obj.approved_by = request.user
            obj.approved_at = timezone.now()
            obj.save()
            self.message_user(request, _('The purchase order has been rejected.'))
            return self.response_post_save_change(request, obj)
        else:
            return super().response_change(request, obj)

    def response_post_save_change(self, request, obj):
        if '_save' in request.POST:
            return super().response_post_save_change(request, obj)
        else:
            return self.response_change(request, obj)

    def get_view_url(self, obj):
        return reverse_lazy('admin:inventory_purchaseorder_view', args=[obj.pk])

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['view_url'] = self.get_view_url(PurchaseOrder.objects.get(pk=object_id))
        return super().change_view(request, object_id, form_url, extra_context=extra_context)


@register(PurchaseOrderItem)
class PurchaseOrderItemAdmin(ModelAdmin):
    list_display = ('id', 'purchase_order', 'vendor_material', 'vendor_equipment', 'quantity', 'vendor_price', 'price')
    list_filter = ('purchase_order__status',)
    search_fields = ('purchase_order__id', 'vendor_material__material__name', 'vendor_equipment__equipment__name')
    autocomplete_fields = ('vendor_material', 'vendor_equipment')

