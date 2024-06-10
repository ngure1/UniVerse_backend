from . import models
from . import serializers
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

    # list all jobs* // create a new job
class ListCreateJob(generics.ListCreateAPIView, GetUserProfileAndPostMixin):
    queryset=models.Job.objects.all().order_by('-created_at')
    serializer_class=serializers.JobSerializer
    permission_classes=[IsAuthenticatedOrReadOnly]
    pagination_class=CustomPagination
    
    def perform_create(self, serializer):
        user_profile = self.get_user_profile()
        serializer.save(author=user_profile)
   
   
    # retrieve a single instance of job, update and delete
class JobDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Job.objects.all().order_by('-created_at')
    serializer_class = serializers.JobSerializer
    permission_classes = [IsOwnerOrReadOnly]


    # get all jobs posts created by a specific user
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


class JobSearchView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = serializers.JobSerializer

    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q', '')

        if not query:
            return Response({'error': _('Query parameter "q" is required.')}, status=status.HTTP_400_BAD_REQUEST)

        job_results = models.Job.objects.filter(
            Q(author__user__first_name__icontains=query) |
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(application_deadline__icontains=query)
        ).order_by('-created_at')

        job_serializer = self.get_serializer(job_results, many=True)

        return Response({'jobs': job_serializer.data})

    
    