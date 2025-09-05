from django.core.exceptions import PermissionDenied
from django.db import models

# Create your models here.
class Currency(models.Model):
    name        = models.CharField(max_length=50, null=True, blank=True)
    code        = models.CharField(max_length=10)
    conversion_rate = models.FloatField(default=1, verbose_name='Coversion rate (USD to ...)')

    def __str__(self):
        return self.code
    
    def delete(self, using, keep_parents):
        if self.pk == 1:
            raise PermissionDenied("You cannot delete default model with id 1")
        return super().delete(using, keep_parents)