from rest_framework import serializers

from inventory.models import Brand


class BrandSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'url', 'name']