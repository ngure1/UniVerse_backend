from . import models
from . import serializers
from .mixins import *
from accounts.models import UserProfile
from posts.mixins import GetUserProfileAndPostMixin
from accounts.pagination import CustomPagination
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from posts.permissions import IsOwnerOrReadOnly
from rest_framework.exceptions import NotFound
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


class ListCreateJob(generics.ListCreateAPIView, GetUserProfileAndPostMixin):
    queryset=models.Job.objects.all().order_by('-created_at')
    serializer_class=serializers.JobSerializer
    permission_classes=[IsAuthenticatedOrReadOnly]
    pagination_class=CustomPagination
    
    def perform_create(self, serializer):
        user_profile = self.get_user_profile()
        serializer.save(author=user_profile)
   
   
    
class JobDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Job.objects.all().order_by('-created_at')
    serializer_class = serializers.JobSerializer
    permission_classes = [IsOwnerOrReadOnly]



class UserJobsList(generics.ListAPIView):
    serializer_class = serializers.JobSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        try:
            user_profile = UserProfile.objects.get(user__id=user_id)
            jobs = models.Job.objects.filter(author=user_profile).order_by('-created_at')
            if not jobs.exists():
                raise NotFound("This user does not have any job postings.")
            return jobs
        except UserProfile.DoesNotExist:
            raise NotFound("User profile does not exist")

       
class CreateBookmarks(generics.CreateAPIView, GetUserProfileAndPostMixin):
   queryset = models.Bookmark.objects.all().order_by('-created_at')
   serializer_class = serializers.BookmarkSerializer
   permission_classes = [IsAuthenticatedOrReadOnly]
   
   def perform_create(self, serializer):
       user_profile = self.get_user_profile()
       job = self.get_job()
       if models.Bookmark.objects.filter(job=job, author=user_profile).exists():
           raise serializers.ValidationError(_("You have already bookmarked this job post."))
       serializer.save(author=user_profile, job=job)
    
class UnbookmarkJob(generics.GenericAPIView, GetUserProfileAndJobMixin):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def delete(self, request, *args, **kwargs):
        user_profile = self.get_user_profile()
        job = self.get_job()

        try:
            bookmark = models.Bookmark.objects.get(job=job, author=user_profile)
            bookmark.delete()
            return Response({"detail": "Unbookmarked the job successfully."}, status=status.HTTP_204_NO_CONTENT)
        except models.Bookmark.DoesNotExist:
            return Response({"detail": "Bookmark does not exist."}, status=status.HTTP_400_BAD_REQUEST)


class JobSearchView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = serializers.JobSerializer

    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q', '')
        job_type = self.request.GET.get('job_type', None)  
        sort_by = self.request.GET.get('sort_by', '-created_at')  

        if not query:
            return Response({'error': _('Query parameter "q" is required.')}, status=status.HTTP_400_BAD_REQUEST)

        # Filter jobs based on the search query and additional parameters
        job_results = models.Job.objects.filter(
            Q(job_title__icontains=query) |
            Q(job_description__icontains=query) |
            Q(job_skills__icontains=query) |
            Q(job_qualifications__icontains=query) |
            Q(address__icontains=query) |
            Q(application_deadline__icontains=query) 
        )

        # Filter by job type if provided
        if job_type in dict(models.Job.JOB_TYPE_CHOICES).keys():
            job_results = job_results.filter(job_type=job_type)

        # Sort jobs based on the provided sort_by parameter
        if sort_by in ['created_at', 'updated_at', 'application_deadline']:
            job_results = job_results.order_by(f'-{sort_by}')
        else:
            job_results = job_results.order_by('-created_at')  


        job_serializer = self.get_serializer(job_results, many=True)
        return Response({'jobs': job_serializer.data})

    
    