from django.contrib.admin import TabularInline, register, ModelAdmin, StackedInline
from django.db import models
from django.forms import TextInput
from django.utils.translation import gettext_lazy as _
from common.admin import TaskInline, QuestionInline
from orders.models import Job, JobService, JobMaterial, JobProduct
from orders.models.warranty import Warranty
from orders.models.service import RequiredServiceMaterial, SuggestedServiceMaterial, ServiceProduct, \
    ServiceMaterialClass, Service, ServiceWarranty


class RequiredServiceMaterialInline(TabularInline):
    model = RequiredServiceMaterial
    extra = 1


class SuggestedServiceMaterialInline(TabularInline):
    model = SuggestedServiceMaterial
    extra = 1


class WarrantyInline(StackedInline):
    model = ServiceWarranty


class ServiceProductInline(TabularInline):
    model = ServiceProduct
    extra = 1


class ServiceMaterialClassInline(TabularInline):
    model = ServiceMaterialClass
    extra = 1


@register(Service)
class ServiceAdmin(ModelAdmin):
    inlines = [RequiredServiceMaterialInline, SuggestedServiceMaterialInline, ServiceProductInline,
               ServiceMaterialClassInline, TaskInline, QuestionInline]
    list_display = ('name', 'price', 'is_active', 'get_targets', 'warranty', 'price',)
    filter_horizontal = ('targets',)
    search_fields = ('name',)
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
    }

    def get_targets(self, obj):
        return ", ".join([t.name for t in obj.targets.all()])

    get_targets.short_description = 'Targets'


@register(RequiredServiceMaterial)
class RequiredServiceMaterialAdmin(ModelAdmin):
    list_display = ['service', 'material', 'quantity']
    search_fields = ['service__name', 'material__name']
    list_filter = ['service__name', 'material__name']


@register(SuggestedServiceMaterial)
class SuggestedServiceMaterialAdmin(ModelAdmin):
    list_display = ['service', 'material', 'quantity']
    search_fields = ['service__name', 'material__name']
    list_filter = ['service__name', 'material__name']


@register(ServiceProduct)
class ServiceProductAdmin(ModelAdmin):
    list_display = ['service', 'product', 'quantity']
    search_fields = ['service__name', 'product__name']
    list_filter = ['service__name', 'product__name']


@register(ServiceMaterialClass)
class ServiceMaterialClassAdmin(ModelAdmin):
    list_display = ['service', 'material_class']
    search_fields = ['service__name', 'material_class__name']
    list_filter = ['service__name', 'material_class__name']


@register(ServiceWarranty)
class WarrantyAdmin(ModelAdmin):
    ...


@register(Warranty)
class WarrantyTemplateAdmin(ModelAdmin):
    inlines = [WarrantyInline]


class JobServiceInline(TabularInline):
    model = JobService
    extra = 0

    autocomplete_fields = ('service', )


class JobMaterialInline(TabularInline):
    model = JobMaterial
    extra = 0

    autocomplete_fields = ('material', )


class JobProductInline(TabularInline):
    model = JobProduct
    extra = 0

    autocomplete_fields = ('product', )


@register(Job)
class JobAdmin(ModelAdmin):
    list_display = ('name', 'customer', 'scheduled_start_time', 'scheduled_end_time', 'status', 'sub_status')
    list_filter = ('status', 'sub_status')
    search_fields = ('name', 'customer__name')
    autocomplete_fields = ('customer',)
    inlines = (JobServiceInline, JobMaterialInline, JobProductInline)
    fieldsets = (
        (None, {'fields': ('name', 'description', 'status', 'sub_status')}),
        (_('Scheduled Time'), {'fields': ('scheduled_start_time', 'scheduled_end_time')}),
        (_('Actual Time'), {'fields': ('actual_start_time', 'actual_end_time')}),
        (_('Technicians'), {'fields': ('technicians',)}),
        (_('Customer'), {'fields': ('customer',)}),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('services', 'materials', 'products')

@register(JobService)
class JobServiceAdmin(ModelAdmin):
    list_display = ('job', 'service', 'quantity')
    list_filter = ('job', 'service')
    search_fields = ('job__name', 'service__name')


@register(JobMaterial)
class JobMaterialAdmin(ModelAdmin):
    list_display = ('job', 'material', 'quantity')
    list_filter = ('job', 'material')
    search_fields = ('job__name', 'material__name')


@register(JobProduct)
class JobProductAdmin(ModelAdmin):
    list_display = ('job', 'product', 'quantity')
    list_filter = ('job', 'product')
    search_fields = ('job__name', 'product__name')