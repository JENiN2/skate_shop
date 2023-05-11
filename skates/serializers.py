from rest_framework import serializers
from .models import Skate


class SkateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skate
        fields = ['name', 'description', 'price', 'article_number', 'color', 'exist']
