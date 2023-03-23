from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.utils.translation import gettext_lazy as _

from customers.models.customer import Customer, BillingLocation, ServiceLocation


class BillingLocationInline(admin.StackedInline):
    model = BillingLocation
    fields = ('name', 'street_address', 'address_line_2', 'city', 'state', 'postal_code')
    extra = 1
    max_num = 1


class ServiceLocationInline(admin.TabularInline):
    model = ServiceLocation
    fields = ('name', 'street_address', 'address_line_2', 'city', 'state', 'postal_code', 'is_primary')
    extra = 1


class ServiceLocationAdmin(admin.ModelAdmin):
    list_display = ('customer', 'is_active', 'is_primary',)
    search_fields = ('name', 'customer__company_name', 'customer__first_name', 'customer__last_name',)
    list_filter = ('is_active',)
    inlines = [ServiceLocationInline]


class BillingLocationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class CustomerContactInline(admin.TabularInline):
    model = Customer.contacts.through
    autocomplete_fields = ['contact']
    extra = 1


class CustomerAdmin(ModelAdmin):
    search_fields = ('company_name', 'first_name', 'last_name',)
    list_filter = ('customer_type',)
    inlines = [CustomerContactInline, BillingLocationInline, ServiceLocationInline]
    list_display = ('name', 'customer_type', 'parent',)
    fieldsets = (
        (None, {
            'fields': ('customer_type', 'parent', 'company_name')
        }),
        (_('Basic Info'), {
            'fields': ('first_name', 'last_name', 'email', 'phone_number')
        }),
    )


admin.site.register(Customer, CustomerAdmin)
admin.site.register(BillingLocation, BillingLocationAdmin)
