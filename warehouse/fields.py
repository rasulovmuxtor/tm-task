from django.core.validators import ValidationError
from django.db import models


def _greater_than_zero(value):
    if value <= 0:
        raise ValidationError('The value should be greater than zero.')


class PositiveDecimalField(models.DecimalField):
    default_validators = [_greater_than_zero]
