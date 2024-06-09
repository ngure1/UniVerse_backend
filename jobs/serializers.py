from accounts.serializers import UserProfileSimpleSerializer
from rest_framework import serializers
from . import models



class JobSerializer(serializers.ModelSerializer):
    author=UserProfileSimpleSerializer(read_only=True)
    url=serializers.HyperlinkedIdentityField(view_name="job-detail", lookup_field="pk")
    class Meta:
        model=models.Job
        fields=(
            "id",
            "url",
            "author",
            "title",
            "description",
            "application_procedure",
            "application_deadline",
            "created_at",
            "updated_at",
        )
        read_only_fields = ('created_at', 'updated_at')
   