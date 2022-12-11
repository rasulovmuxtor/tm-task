from rest_framework import serializers

from warehouse import models

from warehouse.utils import get_warehouses_for_products


class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ['id', 'title', 'code']


class CreateProductSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=models.Product.objects.prefetch_related('materials')
    )
    quantity = serializers.IntegerField(min_value=1)
