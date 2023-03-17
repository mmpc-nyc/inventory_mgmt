from django.db import models


# TODO  Fix the warranty model. This doesn't work properly
class Warranty(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return f'{self.name}'
