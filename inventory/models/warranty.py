from django.db import models


# TODO  Fix the warranty model. This doesn't work propertly
class Warranty(models.Model):
    service = models.OneToOneField('Service', on_delete=models.CASCADE)
    template = models.ForeignKey('WarrantyTemplate', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.template.name} ({self.service.name})'


class WarrantyTemplate(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return f'{self.name}'
