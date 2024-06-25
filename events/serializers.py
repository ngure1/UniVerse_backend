from rest_framework import serializers
from .models import Event
from accounts.serializers import UserProfileSimpleSerializer

class EventSerializer(serializers.ModelSerializer):
    author = UserProfileSimpleSerializer(read_only=True)
    url=serializers.HyperlinkedIdentityField(view_name='event-detail',lookup_field='pk')
    class Meta:
        model = Event
        fields = (
            "id",
            "url",
            "is_online",
            "is_physical",
            "author",
            "title",
            "description",
            "media",
            "address",
            "venue",
            "event_form_url",
            "event_start_date",
            "event_start_time",
            "event_end_date",
            "event_end_time",
            
            "created_at",
            "updated_at",
        )
        read_only_fields = ('created_at', 'updated_at')
