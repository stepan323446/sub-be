from typing import ClassVar
from django.db.models.manager import BaseManager
from django.db import models

from users.models import User
from .managers import PaymentMethodManager

# Create your models here.
class Label(models.Model):
    name        = models.CharField(max_length=50)
    colorHex    = models.CharField(max_length=10)
    user        = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} by {self.user}"
    
    class Meta:
        ordering = ['name']
    
class PaymentMethodType(models.Model):
    type        = models.CharField(max_length=30)
    icon        = models.ImageField(upload_to='card-types/')

    def __str__(self):
        return self.type

    class Meta:
        ordering = ['type']

class PaymentMethod(models.Model):
    name        = models.CharField(max_length=50)
    type        = models.ForeignKey(PaymentMethodType, on_delete=models.SET_NULL, null=True)
    user        = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    objects: PaymentMethodManager["PaymentMethod"] = PaymentMethodManager()

    def __str__(self):
        return f"{self.name} by {self.user}"
    
    class Meta:
        ordering = ['name']