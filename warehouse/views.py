from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from warehouse import models, serializers
from warehouse.utils import get_warehouses_for_products
from warehouse import schema


class ProductListAPIView(ListAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductModelSerializer


class ProductMaterialAPIView(APIView):
    serializer_class = serializers.CreateProductSerializer

    @extend_schema(
        request=serializer_class(many=True),
        responses=schema.ProductMaterialsSerializer(many=True)
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        data = get_warehouses_for_products(serializer.validated_data)
        return Response(data, status=status.HTTP_200_OK)
