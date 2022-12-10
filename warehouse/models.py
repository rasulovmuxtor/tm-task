from django.db import models

from warehouse.fields import PositiveDecimalField


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Product(BaseModel):
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=64)

    class Meta:
        ordering = ['title']
        unique_together = ['title', 'code']

    def __str__(self):
        return self.title


class Material(BaseModel):
    title = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class ProductMaterial(BaseModel):
    product = models.ForeignKey(Product, models.CASCADE,
                                related_name='materials')
    material = models.ForeignKey(Material, models.CASCADE)
    quantity = PositiveDecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ['product', 'material']


class Warehouse(BaseModel):
    material = models.ForeignKey(Material, models.CASCADE)
    remainder = PositiveDecimalField(max_digits=10, decimal_places=2)
    price = PositiveDecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['-id']
