from rest_framework import serializers
from . import models
from accounts.serializers import UserProfileSerializer

class AnnouncementSerializer(serializers.ModelSerializer):
    creator=UserProfileSerializer(read_only=True)
    class Meta:
        model=models.Announcement
        fields=(
            "id",
            "creator",
            "title",
            "content",
            "created_at",
            "updated_at",
            "media"
        )
        read_only_fields = ('created_at', 'updated_at')



