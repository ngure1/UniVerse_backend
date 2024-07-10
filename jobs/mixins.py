from accounts.models import UserProfile
from . import models
from rest_framework.exceptions import NotFound

class GetUserProfileAndJobMixin:
    def get_user_profile(self):
        user = self.request.user
        try:
            return UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            raise NotFound("User profile does not exist")

    def get_job(self):
        job_id = self.kwargs.get('job_id')
        try:
            return models.Job.objects.get(pk=job_id)
        except models.Job.DoesNotExist:
            raise NotFound("Job does not exist")
