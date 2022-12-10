from django.contrib import admin
from django.db.models import F

from warehouse import models


class ProductMaterialInlineAdmin(admin.TabularInline):
    model = models.ProductMaterial
    extra = 0
    autocomplete_fields = ['material']


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'code']
    search_fields = ['title', 'code']
    inlines = [ProductMaterialInlineAdmin]


@admin.register(models.Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    search_fields = ['title']


@admin.register(models.ProductMaterial)
class ProductMaterialAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_title', 'material_title', 'quantity']
    search_fields = ['product__title', 'material__title']
    autocomplete_fields = ['product', 'material']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(product_title=F('product__title'),
                                 material_title=F('material__title'))

    def product_title(self, obj) -> str:
        return obj.product_title

    product_title.short_description = 'Product'  # type: ignore

    def material_title(self, obj) -> str:
        return obj.material_title

    material_title.short_description = 'Material'  # type: ignore


@admin.register(models.Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['id', 'material_title', 'remainder', 'price', 'created_at']
    search_fields = ['material__title']
    autocomplete_fields = ['material']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(material_title=F('material__title'))

    def material_title(self, obj) -> str:
        return obj.material_title

    material_title.short_description = 'Material'  # type: ignore
