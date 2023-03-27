from django.db import models


class AssetRequirementCategory(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)


class MaterialRequirement(models.Model):
    material = models.ForeignKey('inventory.Material', on_delete=models.CASCADE)
    asset_requirement_category = models.ForeignKey(AssetRequirementCategory, on_delete=models.CASCADE)
    minimum_amount = models.PositiveIntegerField(default=0)
    maximum_amount = models.PositiveIntegerField(default=0)


class EquipmentItemRequirement(models.Model):
    equipment_item = models.ForeignKey('inventory.EquipmentItem', on_delete=models.CASCADE)
    asset_requirement_category = models.ForeignKey(AssetRequirementCategory, on_delete=models.CASCADE)
    minimum_amount = models.PositiveIntegerField(default=0)
    maximum_amount = models.PositiveIntegerField(default=0)
