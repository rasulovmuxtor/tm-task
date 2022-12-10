from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.renderers import JSONOpenAPIRenderer, JSONRenderer
from rest_framework.response import Response

from warehouse import models, serializers
from warehouse.utils import get_warehouses_for_products


class ProductListAPIView(ListAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductModelSerializer


class ProductMaterialAPIView(CreateAPIView):
    serializer_class = serializers.CreateProductSerializer
    # swagger schema properties
    pagination_class = None
    filter_backends = []  # type: ignore
    renderer_classes = [JSONOpenAPIRenderer, JSONRenderer]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = self.get_response_data(serializer.validated_data)
        return Response(data, status=status.HTTP_200_OK)

    def get_response_data(self, validated_data: list) -> dict:
        results = get_warehouses_for_products(validated_data)
        return {'results': results}

    def get_serializer(self, *args, **kwargs):
        kwargs.setdefault('many', True)  # swagger schema is generated based
        return self.serializer_class(*args, **kwargs)
