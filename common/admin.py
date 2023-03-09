from django.contrib import admin

# Register your models here.
from django.contrib.admin import register, ModelAdmin

from common.models.contact import Contact, PhoneNumber, ContactEmail, ContactPhoneNumber
from common.models.field import Field
from common.models.location import Location


@register(Field)
class FieldAdmin(ModelAdmin):
    list_display = ['name', 'content_type', 'field_type', 'validation_type', 'default_value', 'is_required']


@register(Contact)
class ContactAdmin(ModelAdmin):
    list_display = ('first_name', 'last_name',)


@register(Location)
class LocationAdmin(ModelAdmin):
    ...


@register(PhoneNumber)
class PhoneNumberAdmin(ModelAdmin):
    ...


@register(ContactEmail)
class ContactEmailAdmin(ModelAdmin):
    list_display = ('contact', 'email',)


@register(ContactPhoneNumber)
class ContactPhoneNumberAdmin(ModelAdmin):
    list_display = ('contact', 'phone_number',)