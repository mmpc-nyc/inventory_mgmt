# from django.contrib.admin import TabularInline, register, ModelAdmin, StackedInline
# from django.db import models
# from django.forms import TextInput
#
# from inventory.models.warranty import Warranty, WarrantyTemplate
# from orders.models.service import RequiredServiceMaterial, SuggestedServiceMaterial, ServiceProduct, \
#     ServiceMaterialClass, Service
#
#
# class RequiredServiceMaterialInline(TabularInline):
#     model = RequiredServiceMaterial
#     extra = 1
#
#
# class SuggestedServiceMaterialInline(TabularInline):
#     model = SuggestedServiceMaterial
#     extra = 1
#
#
# class WarrantyInline(StackedInline):
#     model = Warranty
#
#
# class ServiceProductInline(TabularInline):
#     model = ServiceProduct
#     extra = 1
#
#
# class ServiceMaterialClassInline(TabularInline):
#     model = ServiceMaterialClass
#     extra = 1
#
#
# @register(Service)
# class ServiceAdmin(ModelAdmin):
#     inlines = [RequiredServiceMaterialInline, SuggestedServiceMaterialInline, ServiceProductInline,
#                ServiceMaterialClassInline]
#     list_display = ('name', 'price', 'is_active')
#     search_fields = ('name',)
#     formfield_overrides = {
#         models.CharField: {'widget': TextInput(attrs={'size': '20'})},
#     }
#
#
# @register(RequiredServiceMaterial)
# class RequiredServiceMaterialAdmin(ModelAdmin):
#     list_display = ['service', 'material', 'quantity']
#     search_fields = ['service__name', 'material__name']
#     list_filter = ['service__name', 'material__name']
#
#
# @register(SuggestedServiceMaterial)
# class SuggestedServiceMaterialAdmin(ModelAdmin):
#     list_display = ['service', 'material', 'quantity']
#     search_fields = ['service__name', 'material__name']
#     list_filter = ['service__name', 'material__name']
#
#
# @register(ServiceProduct)
# class ServiceProductAdmin(ModelAdmin):
#     list_display = ['service', 'product', 'quantity']
#     search_fields = ['service__name', 'product__name']
#     list_filter = ['service__name', 'product__name']
#
#
# @register(ServiceMaterialClass)
# class ServiceMaterialClassAdmin(ModelAdmin):
#     list_display = ['service', 'material_class']
#     search_fields = ['service__name', 'material_class__name']
#     list_filter = ['service__name', 'material_class__name']
#
#
# @register(Warranty)
# class WarrantyAdmin(ModelAdmin):
#     ...
#
#
# @register(WarrantyTemplate)
# class WarrantyTemplateAdmin(ModelAdmin):
#     inlines = [WarrantyInline]
