from accounts.serializers import UserProfileSerializer
from rest_framework import serializers
from . import models



class JobSerializer(serializers.ModelSerializer):
    job_owner=UserProfileSerializer(read_only=True)
    class Meta:
        model=models.Job
        fields=(
            "id",
            "job_owner",
            "title",
            "description",
            "application_procedure",
            "application_deadline",
            "created_at",
            "updated_at",
        )
        read_only_fields = ('created_at', 'updated_at')
   