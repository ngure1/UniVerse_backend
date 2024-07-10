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
            "job_title",
            "job_description",
            "job_skills",
            "job_qualifications",
            "job_type",
            "address",
            "media",
            "application_procedure",
            "application_deadline",
            "application_link",
            "created_at",
            "updated_at",
        )
        read_only_fields = ('created_at', 'updated_at')
        
class BookmarkSerializer(serializers.ModelSerializer):
   job=JobSerializer(read_only=True)
   author = UserProfileSimpleSerializer(read_only=True)
  
   class Meta:
       model = models.Bookmark
       fields = (
           "id",
           "author",
           "job",
           "created_at",
           "updated_at"
       )
       read_only_fields=('creatd_at','updated_at')
   