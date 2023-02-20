from django.contrib.admin import register, ModelAdmin
from mptt.admin import MPTTModelAdmin

from inventory.models.location import Location
from inventory.models.stock_location import StockLocation
from inventory.models.contact import Contact, ContactPhoneNumber, ContactEmail, PhoneNumber
from inventory.models.customer import Customer, ServiceLocation
from inventory.models.product import Product, ProductType, Brand, InterchangeableProduct, Category
from inventory.models.equipment import Equipment, Condition


@register(ServiceLocation)
class CustomerLocationAdmin(ModelAdmin):
    list_display = ('customer', 'location')


@register(ContactEmail)
class ContactEmailAdmin(ModelAdmin):
    list_display = ('contact', 'email',)


@register(ContactPhoneNumber)
class ContactPhoneNumberAdmin(ModelAdmin):
    list_display = ('contact', 'phone_number',)


@register(InterchangeableProduct)
class InterchangeableProductAdmin(ModelAdmin):
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
    list_display = ('name', 'brand', 'interchangeable_product', 'status',)
    history_list_display = list_display


@register(Equipment)
class EquipmentAdmin(ModelAdmin):
    list_display = ('id', 'name', 'status', 'condition', 'warehouse', 'location', 'user',)


@register(StockLocation)
class StockLocationAdmin(ModelAdmin):
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


@register(Location)
class LocationAdmin(ModelAdmin):
    ...


@register(PhoneNumber)
class PhoneNumberAdmin(ModelAdmin):
    ...


@register(Condition)
class ConditionAdmin(ModelAdmin):
    list_display = ['name', 'description']