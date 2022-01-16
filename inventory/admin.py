from django.contrib.admin import register, ModelAdmin, TabularInline
from mptt.admin import MPTTModelAdmin

from inventory.models.location import Location
from inventory.models.stock import Stock
from inventory.models.contact import Contact, ContactPhoneNumber, ContactEmail, PhoneNumber
from inventory.models.customer import Customer, CustomerLocation, CustomerContact
from inventory.models.equipment import Equipment, Condition, EquipmentTransaction
from inventory.models.product import Product, ProductType, Brand, GenericProduct, Category
from inventory.models.order import Order, OrderGenericProduct


class GenericProductInline(TabularInline):
    model = OrderGenericProduct


@register(CustomerLocation)
class CustomerLocationAdmin(ModelAdmin):
    list_display = ('customer', 'location')


@register(ContactEmail)
class ContactEmailAdmin(ModelAdmin):
    list_display = ('contact', 'email',)


@register(ContactPhoneNumber)
class ContactPhoneNumberAdmin(ModelAdmin):
    list_display = ('contact', 'phone_number',)


@register(GenericProduct)
class GenericProductAdmin(ModelAdmin):
    list_display = ('name',)
    list_filter = ('name', 'category',)
    search_fields = ('category__name',)


@register(Customer)
class CustomerAdmin(MPTTModelAdmin):
    list_display = ('first_name', 'last_name', 'company_name', 'parent')


@register(Contact)
class ContactAdmin(ModelAdmin):
    list_display = ('first_name', 'last_name',)


@register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ('name', 'brand', 'product_type', 'generic_product', 'status', 'count',)
    history_list_display = list_display


@register(Equipment)
class EquipmentAdmin(ModelAdmin):
    list_display = ('id', 'name', 'status', 'condition', 'stock', 'location', 'user',)
    readonly_fields = ('counter',)


@register(Stock)
class StockAdmin(ModelAdmin):
    list_display = ('name', 'status', 'location',)


@register(Category)
class CategoryAdmin(MPTTModelAdmin):
    ...


@register(ProductType)
class ProductTypeAdmin(ModelAdmin):
    list_display = ('name',)


@register(Brand)
class BrandAdmin(ModelAdmin):
    list_display = ('name',)


@register(OrderGenericProduct)
class OrderGenericProductAdmin(ModelAdmin):
    ...


@register(Location)
class LocationAdmin(ModelAdmin):
    ...


@register(PhoneNumber)
class PhoneNumberAdmin(ModelAdmin):
    ...


@register(Order)
class OrderAdmin(ModelAdmin):
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


@register(EquipmentTransaction)
class EquipmentTransactionAdmin(ModelAdmin):
    ...