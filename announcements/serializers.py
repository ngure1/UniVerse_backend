from rest_framework import serializers
from . import models
from accounts.serializers import UserProfileSerializer

class AnnouncementSerializer(serializers.ModelSerializer):
    creator=UserProfileSerializer(read_only=True)
    url=serializers.HyperlinkedIdentityField(view_name="announcement-detail", lookup_field="pk")
    
    class Meta:
        model=models.Announcement
        fields=(
            "id",
            "url",
            "creator",
            "title",
            "media",
            "content",
            "created_at",
            "updated_at",
        )
        read_only_fields = ('created_at', 'updated_at')



