from django.contrib.admin import register, ModelAdmin, TabularInline
from mptt.admin import MPTTModelAdmin
from simple_history.admin import SimpleHistoryAdmin

from inventory.models import Contact, ContactPhoneNumber, ContactEmail, PhoneNumber, Location, Customer, \
    CustomerLocation, CustomerContact, Equipment, Condition, GenericProduct, Category, Product, ProductType, Brand, \
    Stock
from inventory.models import Order, OrderGenericProduct


class GenericProductInline(TabularInline):
    model = OrderGenericProduct


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
class ProductAdmin(ModelAdmin):
    list_display = ('name', 'brand', 'product_type', 'generic_product', 'status', 'count',)
    history_list_display = list_display


@register(Equipment)
class EquipmentAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'name', 'status', 'condition', 'stock', 'user',)
    readonly_fields = ('counter',)


@register(Stock)
class StockAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'status', 'location',)


@register(Category)
class CategoryAdmin(MPTTModelAdmin):
    ...


@register(ProductType)
class ProductTypeAdmin(SimpleHistoryAdmin):
    list_display = ('name',)


@register(Brand)
class BrandAdmin(SimpleHistoryAdmin):
    list_display = ('name',)


@register(OrderGenericProduct)
class OrderGenericProductAdmin(ModelAdmin):
    ...


@register(Location)
class LocationAdmin(SimpleHistoryAdmin):
    ...


@register(PhoneNumber)
class PhoneNumberAdmin(ModelAdmin):
    ...


@register(Order)
class OrderAdmin(SimpleHistoryAdmin):
    list_display = ['id', 'activity', 'customer', 'location', 'date', 'user_names', 'status']
    inlines = (GenericProductInline,)

    @staticmethod
    def user_names(obj: Order):
        return ', '.join(user.username for user in obj.users.all())


@register(CustomerContact)
class CustomerContactAdmin(ModelAdmin):
    ...


@register(Condition)
class ConditionAdmin(ModelAdmin):
    list_display = ['name', 'description']
