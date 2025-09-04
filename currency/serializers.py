from rest_framework import serializers
from .models import Currency

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ('pk', 'name', 'code', 'conversion_rate')

class CurrencyListSerializer(serializers.Serializer):
    currencies = CurrencySerializer(many=True, read_only=True)