from rest_framework import serializers


class ProductMaterialsSerializer(serializers.Serializer):
    class Materials(serializers.Serializer):
        warehouse_id = serializers.IntegerField(required=False)
        material_name = serializers.CharField()
        qty = serializers.DecimalField(max_digits=10, decimal_places=2)
        price = serializers.DecimalField(max_digits=10, decimal_places=2,
                                         required=False)

    product_name = serializers.CharField()
    product_qty = serializers.DecimalField(max_digits=10, decimal_places=2)
    product_materials = Materials(many=True)
