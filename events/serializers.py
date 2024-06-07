from rest_framework import serializers
from . import models
from accounts.serializers import UserProfileSerializer


class EventSerializer(serializers.ModelSerializer):
    creator = UserProfileSerializer(read_only=True)

    class Meta:
        model = models.Event
        fields = (
            "id",
            "creator",
            "title",
            "description",
            "created_at",
            "updated_at",
            "address",
            "media",
            "capacity"


        )
        read_only_fields = ('created_at', 'updated_at')