from . import models
from rest_framework import serializers
from accounts.serializers import UserProfileSerializer


class SupportSerializer(serializers.ModelSerializer):
    owner=UserProfileSerializer(read_only=True)
    url=serializers.HyperlinkedIdentityField(view_name="support-detail", lookup_field="pk")
    class Meta:
        model = models.Support
        fields = [
            'id',
            'url',
            'owner',
            'title',
            'description',
            'amount',
            'created_at',
            'updated_at'
            
        ]
        read_only_fields=(
            'created_at',
            'updated_at'
        )

