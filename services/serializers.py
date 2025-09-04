from rest_framework import serializers
from .models import Service

class ServiceSerializer(serializers.ModelSerializer):
    url = serializers.URLField()

    class Meta:
        model = Service
        fields = ['pk', 'name', 'url', 'icon', 'user', 'created_at', 'updated_at']
        read_only_fields = ("user", 'icon', 'created_at', 'updated_at')