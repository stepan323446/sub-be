from django.db import models
from drf_spectacular.utils import extend_schema

# Create your models here.
class Currency(models.Model):
    name        = models.CharField(max_length=50, null=True, blank=True)
    code        = models.CharField(max_length=10)
    conversion_rate = models.FloatField(default=1, verbose_name='Coversion rate (USD to ...)')

    def __str__(self):
        return self.code