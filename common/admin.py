from django.contrib.admin import register, ModelAdmin, TabularInline
from django.contrib.contenttypes.admin import GenericTabularInline
from django.urls import reverse
from django.utils.html import format_html
from mptt.admin import DraggableMPTTAdmin

from common.models.address import Address
from common.models.contact import Contact, ContactEmail, ContactPhoneNumber
from common.models.document import Document
from common.models.field import Field
from common.models.question import Question
from common.models.target import Target
from common.models.task import Task
from common.models.unit import UnitCategory, Unit


@register(Field)
class FieldAdmin(ModelAdmin):
    list_display = ['name', 'content_type', 'field_type', 'validation_type', 'default_value', 'is_required']


@register(Address)
class AddressAdmin(ModelAdmin):
    list_display = ('name', 'street_address', 'city', 'state', 'postal_code',)
    search_fields = ('name', 'street_address', 'city', 'state', 'postal_code',)
    list_filter = ('state',)
    ordering = ('name', 'street_address',)
    fieldsets = (
        (None, {
            'fields': ('name', 'street_address', 'address_line_2', 'city', 'state', 'postal_code',)
        }),
        ('Geo Location', {
            'fields': ('latitude', 'longitude',),
        }),
    )


@register(ContactEmail)
class ContactEmailAdmin(ModelAdmin):
    list_display = ('contact', 'email', 'email_type', 'is_primary')
    list_filter = ('email_type', 'is_primary')
    search_fields = ('contact__first_name', 'contact__last_name', 'email')
    fieldsets = (
        (None, {
            'fields': ('contact', 'email', 'email_type', 'is_primary')
        }),
    )


@register(ContactPhoneNumber)
class ContactPhoneNumberAdmin(ModelAdmin):
    list_display = ('contact', 'phone_number', 'phone_type', 'is_primary')
    list_filter = ('phone_type', 'is_primary')
    search_fields = ('contact__first_name', 'contact__last_name', 'phone_number')
    fieldsets = (
        (None, {
            'fields': ('contact', 'phone_number', 'phone_type', 'is_primary')
        }),
    )


class ContactPhoneNumberInline(TabularInline):
    model = ContactPhoneNumber
    extra = 1


class ContactEmailInline(TabularInline):
    model = ContactEmail
    extra = 1


@register(Contact)
class ContactAdmin(ModelAdmin):
    list_display = ('first_name', 'last_name')
    search_fields = ('first_name', 'last_name', 'emails__email', 'phone_numbers__phone_number')

    inlines = [ContactPhoneNumberInline, ContactEmailInline]

    def name(self, obj):
        return str(obj)

    name.admin_order_field = 'first_name'


@register(Target)
class TargetAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 10
    mptt_indent_field = 'name'
    search_fields = ('name', )
    list_display = ['tree_actions', 'indented_title', 'material_list']
    list_display_links = ('indented_title',)

    readonly_fields = ('material_list',)

    def material_list(self, obj):
        materials = obj.material_targets.all()
        links = []
        for material in materials:
            url = reverse('admin:inventory_material_change', args=[material.pk])
            link = f'<a href="{url}">{material.name}</a>'
            links.append(link)
        return format_html(', '.join(links))

    material_list.short_description = 'Materials Associated'
    material_list.allow_tags = True


@register(UnitCategory)
class UnitCategoryAdmin(ModelAdmin):
    pass


@register(Unit)
class UnitAdmin(ModelAdmin):
    list_display = ['name', 'abbreviation', 'conversion_factor', 'is_metric']


@register(Document)
class AgreementAdmin(ModelAdmin):
    list_display = ('sender', 'document', 'status', 'date_created')
    list_filter = ('status', 'date_created')
    search_fields = ('sender__username', 'recipients__username', 'document__name')
    readonly_fields = ('date_created', 'date_sent', 'date_completed', 'signature')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(sender=request.user) | qs.filter(recipients=request.user)

    def has_change_permission(self, request, obj=None):
        if obj is not None and not request.user.is_superuser and obj.sender != request.user:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if obj is not None and not request.user.is_superuser and obj.sender != request.user:
            return False
        return True


class TaskInline(GenericTabularInline):
    model = Task
    extra = 1


@register(Task)
class TaskAdmin(ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'status', 'priority', 'assigned_to')
    list_filter = ('status', 'priority')
    search_fields = ('title', 'description', 'location', 'assigned_to__username')
    date_hierarchy = 'start_date'
    ordering = ('-updated_at',)
    fieldsets = (
        (None, {
            'fields': ('title', 'description')
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date')
        }),
        ('Details', {
            'fields': ('status', 'priority', 'location', 'assigned_to')
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('assigned_to')


class QuestionInline(GenericTabularInline):
    model = Question
    extra = 1


@register(Question)
class QuestionAdmin(ModelAdmin):
    list_display = ('text',)


