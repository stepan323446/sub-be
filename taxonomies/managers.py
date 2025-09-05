from typing import TypeVar
from django.db import models

T = TypeVar('T')

class PaymentMethodManager(models.Manager[T]):
    def get_queryset(self):
        return super().get_queryset().select_related('type')