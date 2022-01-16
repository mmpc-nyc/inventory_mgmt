from django.db import models

from inventory.enums import OrderActivity


class OrderManager(models.Manager):
    activity: OrderActivity

    def get_queryset(self):
        qs = super().get_queryset()
        if hasattr(self, 'activity'):
            return qs.filter(activity=self.activity)
        return qs

    def create(self, **kwargs):
        if hasattr(self, 'activity'):
            kwargs.update({'activity': self.activity})
        return super().create(**kwargs)


class CollectOrderManager(OrderManager):
    activity = OrderActivity.COLLECT


class DeployOrderManager(OrderManager):
    activity = OrderActivity.DEPLOY


class InspectOrderManager(OrderManager):
    activity = OrderActivity.INSPECT