from django.db import models


class UnitCategory(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return f'{self.name}'


class Unit(models.Model):
    name = models.CharField(max_length=50)
    abbreviation = models.CharField(max_length=10)
    conversion_factor = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    display_format = models.CharField(max_length=50, blank=True, null=True)
    category = models.ForeignKey(UnitCategory, on_delete=models.CASCADE)
    is_metric = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}'
