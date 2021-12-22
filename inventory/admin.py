from django.contrib.admin import register
from simple_history.admin import SimpleHistoryAdmin

from inventory.models import Product, Location, Stock, GenericProduct, Customer, Contact, Job, Category, ProductType, \
    Brand, CustomerLocation, ContactEmail, ContactPhoneNumber


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


@register(Customer)
class CustomerAdmin(SimpleHistoryAdmin):
    list_display = ('first_name', 'last_name', 'company_name', 'parent')


@register(Contact)
class ContactAdmin(SimpleHistoryAdmin):
    list_display = ('first_name', 'last_name',)


@register(Product)
class ProductAdmin(SimpleHistoryAdmin):
    list_display = ['name', 'job', 'status', 'employee', 'condition', 'inventory', ]
    history_list_display = list_display


@register(Stock)
class InventoryAdmin(SimpleHistoryAdmin):
    ...


@register(Location)
class LocationAdmin(SimpleHistoryAdmin):
    ...


@register(Job)
class JobAdmin(SimpleHistoryAdmin):
    ...


@register(Category)
class CategoryAdmin(SimpleHistoryAdmin):
    ...


@register(ProductType)
class ProductTypeAdmin(SimpleHistoryAdmin):
    ...


@register(Brand)
class BrandAdmin(SimpleHistoryAdmin):
    ...
