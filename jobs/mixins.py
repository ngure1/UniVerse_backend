from accounts.models import UserProfile
from . import models
from rest_framework.exceptions import NotFound, NotAuthenticated

class GetUserProfileAndJobMixin:
    def get_user_profile(self):
        if not self.request.user.is_authenticated:
            raise NotAuthenticated("User is not authenticated.")
        try:
            return UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
            raise NotFound("UserProfile matching query does not exist.")

    def get_job(self):
        job_id = self.kwargs.get('job_id')
        if not job_id:
            raise NotFound("Job ID not provided.")
        try:
            return models.Job.objects.get(pk=job_id)
        except models.Job.DoesNotExist:
            raise NotFound("Job matching query does not exist.")
