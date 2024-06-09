from rest_framework.exceptions import NotFound
from accounts.models import UserProfile
from . import models

class GetUserProfileAndPostMixin:
    def get_user_profile(self):
        try:
            return self.request.user.user_profile
        except UserProfile.DoesNotExist:
            raise NotFound("UserProfile matching query does not exist.")

    def get_post(self):
        post_id = self.request.data.get('post')
        try:
            return models.Post.objects.get(id=post_id)
        except models.Post.DoesNotExist:
            raise NotFound("Post matching query does not exist.")
