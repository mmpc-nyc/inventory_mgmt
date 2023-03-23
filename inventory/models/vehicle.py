from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class Vehicle(models.Model):
    """A vehicle that can hold equipment and materials"""

    class VehicleType(models.TextChoices):
        """Choices for setting the type of a vehicle"""

        PASSENGER = 'Passenger', _('Passenger')
        COMMERCIAL = 'Commercial', _('Commercial')

    driver = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='vehicles', blank=True, null=True)
    vin_number = models.CharField(max_length=50, unique=True)
    license_plate = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=50)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    model_year = models.PositiveSmallIntegerField()
    vehicle_type = models.CharField(max_length=32, choices=VehicleType.choices, default=VehicleType.COMMERCIAL)
    asset_requirement_category = models.ForeignKey(
        'inventory.AssetRequirementCategory',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='vehicles'
    )

    def __str__(self):
        return f'{self.name} ({self.license_plate})'

    def get_vehicle_materials_with_requirements(self):
        # TODO Define this method
        ...

    def get_vehicle_equipment_items_with_requirements(self):
        # TODO Define this method
        ...

    class Meta:
        verbose_name = _('Vehicle')
        verbose_name_plural = _('Vehicles')

    def get_absolute_url(self):
        return reverse_lazy('inventory:vehicle_detail', kwargs={'pk': self.pk})


class VehicleEquipmentItem(models.Model):
    """
    Represents an individual instance of a piece of equipment held by a vehicle.
    """
    equipment_item = models.ForeignKey('inventory.EquipmentItem', on_delete=models.CASCADE)
    vehicle = models.ForeignKey('inventory.Vehicle', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    minimum_quantity = models.PositiveIntegerField(default=0)
    maximum_quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.equipment_item.equipment.name} ({self.vehicle.name})"


class VehicleMaterial(models.Model):
    """
    Represents an individual instance of a material held by a vehicle.
    """
    material = models.ForeignKey('inventory.Material', on_delete=models.CASCADE)
    vehicle = models.ForeignKey('inventory.Vehicle', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    minimum_quantity = models.PositiveIntegerField(default=0)
    maximum_quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.material.name} ({self.vehicle.name})"
