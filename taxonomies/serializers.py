import re
from rest_framework import serializers
from .models import *

COLOR_NO_TRANSPERENT_REGEX = r"^#[0-9A-Fa-f]{6}$"

class LabelSerializer(serializers.ModelSerializer):
    def validate_colorHex(self, value):
        match_color = re.match(COLOR_NO_TRANSPERENT_REGEX, value)
        if not match_color:
            raise serializers.ValidationError({"label": "Color is not valid. It must be hex format without transperency"})

        return value

    class Meta:
        model = Label
        fields = ['pk', 'name', 'colorHex', 'user', 'created_at', 'updated_at']
        read_only_fields = ("user", 'created_at', 'updated_at')

class PaymentMethodTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethodType
        fields = ['pk', 'type', 'icon']

class PaymentMethodSerializer(serializers.ModelSerializer):
    public_name = serializers.SerializerMethodField(read_only=True)
    type_detail = PaymentMethodTypeSerializer(source="type", read_only=True)

    class Meta:
        model = PaymentMethod
        fields = ['pk', 'public_name', 'name', 'type', 'type_detail', 'user', 'created_at', 'updated_at']
        read_only_fields = ("user", "created_at", "updated_at")

    def get_public_name(self, obj: "PaymentMethodSerializer"):
        if obj.name:
            return f"{obj.name} ({obj.type.type})"
        else:
            return obj.type_detail.type
