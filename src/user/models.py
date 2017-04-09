from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from src.user import fields


# Create your models here.
class MyUser(AbstractUser):
    birthday = models.DateField(
        default=timezone.now,
        verbose_name='birthday',
        blank=True,
        null=True,
    )
    random_number = fields.IntegerRangeField(
        min_value=0, max_value=100,
        null=True,
        blank=True,
    )

