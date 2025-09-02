import re
from rest_framework import serializers
from .models import *

COLOR_NO_TRANSPERENT_REGEX = r"^#[0-9A-Fa-f]{6}$"

class LabelSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def validate_colorHex(self, value):
        match_color = re.match(COLOR_NO_TRANSPERENT_REGEX, value)
        if not match_color:
            raise serializers.ValidationError({"label": "Color is not valid. It must be hex format without transperency"})

        return value

    class Meta:
        model = Label
        fields = ['pk', 'name', 'colorHex', 'user', 'created_at', 'updated_at']
        read_only_fields = ("user",)

class PaymentMethodTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethodType
        fields = ['type', 'icon']

class PaymentMethodTypeSerializer(serializers.ModelSerializer):
    type = PaymentMethodTypeSerializer()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = PaymentMethodType
        fields = ['name', 'type', 'user', 'created_at', 'updated_at']
        read_only_fields = ("user",)

