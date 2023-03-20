from django.contrib.admin import register, ModelAdmin
from django.contrib.contenttypes.admin import GenericTabularInline

from common.models.document import Document
from common.models.contact import Contact, PhoneNumber, ContactEmail, ContactPhoneNumber
from common.models.field import Field
from common.models.location import Location
from common.models.question import Question
from common.models.target import Target
from common.models.task import Task
from common.models.unit import UnitCategory, Unit


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


@register(Target)
class TargetAdmin(ModelAdmin):
    list_display = ['name', 'description', 'parent', ]
    ordering = 'parent', 'name'


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
