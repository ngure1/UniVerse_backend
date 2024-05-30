from . import models
from rest_framework import serializers
from accounts.serializers import UserProfileSerializer


class SupportSerializer(serializers.ModelSerializer):
    owner=UserProfileSerializer(read_only=True)
    class Meta:
        model = models.Support
        fields = [
            'title',
            'description',
            'amount',
            'created_at',
            'owner'
        ]
        read_only_fields=(
            'created_at', 
            'updated_at'
        )

