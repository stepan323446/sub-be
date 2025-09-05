from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string

from currency.models import Currency
from datetime import timedelta

def get_default_currency():
    return Currency.objects.get(code='USD').id

# Create your models here.
class User(AbstractUser):
    limit = models.FloatField(default=0)
    currency = models.ForeignKey(Currency, on_delete=models.SET_DEFAULT, default=get_default_currency)
    is_monday_first = models.BooleanField(default=True)

    notification_email_enable = models.BooleanField(default=True)
    news_email_enable = models.BooleanField(default=False)


    def __str__(self):
        return self.username
    
class VerificationCode(models.Model):
    EXPIRATION_MINUTES = 5
    PURPOSE_CHOICES = [
        ('password_reset', 'Password Reset'),
        ('registration_confirm', 'Registration Confirmation'),
    ]

    code = models.CharField(max_length=255, unique=True)
    is_used = models.BooleanField(default=False)
    purpose = models.CharField(max_length=50, choices=PURPOSE_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.purpose} by {self.user} at {self.created_at}'
    
    @property
    def is_available(self):
        last_code = VerificationCode.objects.filter(user=self.user, purpose=self.purpose).order_by('-created_at').first()

        if last_code and last_code.code != self.code:
            return False

        expiration_time = self.created_at + timedelta(minutes=self.EXPIRATION_MINUTES)
        return not self.is_used and timezone.now() < expiration_time

    @staticmethod
    def generate_code(user: User, purpose: str):
        code = get_random_string(length=50)
        verification = VerificationCode(code=code, user=user, purpose=purpose)
        verification.save()

        return verification