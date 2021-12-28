from django.contrib.admin import register
from simple_history.admin import SimpleHistoryAdmin
from mptt.admin import MPTTModelAdmin
from inventory.models import Product, Location, Stock, GenericProduct, Customer, Contact, Order, Category, ProductType, \
    Brand, CustomerLocation, ContactEmail, ContactPhoneNumber, Equipment


@register(CustomerLocation)
class CustomerLocationAdmin(SimpleHistoryAdmin):
    list_display = ('customer', 'location')


@register(ContactEmail)
class ContactEmailAdmin(SimpleHistoryAdmin):
    list_display = ('contact', 'email',)


@register(ContactPhoneNumber)
class ContactPhoneNumberAdmin(SimpleHistoryAdmin):
    list_display = ('contact', 'phone_number',)


@register(GenericProduct)
class GenericProductAdmin(SimpleHistoryAdmin):
    list_display = ('name',)
    list_filter = ('name', 'category',)
    search_fields = ('category__name',)


@register(Customer)
class CustomerAdmin(SimpleHistoryAdmin):
    list_display = ('first_name', 'last_name', 'company_name', 'parent')


@register(Contact)
class ContactAdmin(SimpleHistoryAdmin):
    list_display = ('first_name', 'last_name',)


@register(Product)
class ProductAdmin(SimpleHistoryAdmin):
    list_display = (
        'name',
        'brand',
        'product_type',
        'generic_name',
        'status',
        'stored_count',
        'deployed_count',
        'picked_up_count',
        'decommissioned_count',
        'count',
    )
    history_list_display = list_display


@register(Equipment)
class EquipmentAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'name', 'status', 'stock', 'employee', 'order', )
    readonly_fields = ('counter', 'name',)


@register(Stock)
class StockAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'status', 'location', )


@register(Location)
class LocationAdmin(SimpleHistoryAdmin):
    ...


@register(Order)
class OrderAdmin(SimpleHistoryAdmin):
    ...


@register(Category)
class CategoryAdmin(MPTTModelAdmin):
    ...


@register(ProductType)
class ProductTypeAdmin(SimpleHistoryAdmin):
    list_display = ('name', )


@register(Brand)
class BrandAdmin(SimpleHistoryAdmin):
    list_display = ('name', )
