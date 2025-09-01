from rest_framework.response import Response
from rest_framework import serializers

class DetailSerializer(serializers.Serializer):
    detail = serializers.CharField(max_length=255)

class EmptySerializer(serializers.Serializer):
    pass