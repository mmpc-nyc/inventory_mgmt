from rest_framework import serializers

from inventory.models.product import Brand


class BrandSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'url', 'name']