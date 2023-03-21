from django.db import models

from django.utils.translation import gettext_lazy as _


class Service(models.Model):
    # TODO Check this model to see if it works properly
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    targets = models.ManyToManyField('common.Target', related_name='service_targets')
    material_classes = models.ManyToManyField('inventory.MaterialClass')
    required_materials = models.ManyToManyField('inventory.Material', related_name='services_with_required_materials', blank=True,
                                                through='RequiredServiceMaterial')
    suggested_materials = models.ManyToManyField('inventory.Material', related_name='services_with_suggested_materials', blank=True,
                                                 through='SuggestedServiceMaterial')
    products = models.ManyToManyField('inventory.Material', related_name='services_with_products', blank=True,
                                      through='ServiceProduct')
    warranty = models.ForeignKey('orders.Warranty', on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')


class PricingScheme(models.Model):
    # TODO Define the properties for pricing scheme
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = _('Pricing Scheme')
        verbose_name_plural = _('Pricing Schemes')


class RequiredServiceMaterial(models.Model):
    service = models.ForeignKey('orders.Service', on_delete=models.CASCADE)
    material = models.ForeignKey('inventory.Material', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.material} ({self.quantity})'

    class Meta:
        verbose_name = _('Required Service Material')
        verbose_name_plural = _('Required Service Materials')


class RequiredServiceEquipment(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    material = models.ForeignKey('inventory.Equipment', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.material} ({self.quantity})'

    class Meta:
        verbose_name = _('Required Service Material')
        verbose_name_plural = _('Required Service Materials')


class SuggestedServiceMaterial(models.Model):
    service = models.ForeignKey('orders.Service', on_delete=models.CASCADE)
    material = models.ForeignKey('inventory.Material', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.material} ({self.quantity})'

    class Meta:
        verbose_name = _('Suggested Service Material')
        verbose_name_plural = _('Suggested Service Materials')


class ServiceProduct(models.Model):
    service = models.ForeignKey('orders.Service', on_delete=models.CASCADE)
    product = models.ForeignKey('inventory.Material', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.product} ({self.quantity})'

    class Meta:
        verbose_name = _('Service Product')
        verbose_name_plural = _('Service Products')


class ServiceMaterialClass(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    material_class = models.ForeignKey('inventory.MaterialClass', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Service Material Class')
        verbose_name_plural = _('ServiceMaterialClasses')


class ServiceWarranty(models.Model):
    service = models.OneToOneField('Service', on_delete=models.CASCADE)
    warranty = models.ForeignKey('Warranty', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.warranty.name} ({self.service.name})'

    class Meta:
        verbose_name = _('Service Warranty')
        verbose_name_plural = _('Service Warranties')
