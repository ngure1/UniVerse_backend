from rest_framework.exceptions import NotFound
from accounts.models import UserProfile
from .models import Post
from rest_framework.exceptions import NotAuthenticated

class GetUserProfileAndPostMixin:
    def get_user_profile(self):
        if not self.request.user.is_authenticated:
            raise NotAuthenticated("User is not authenticated.")
        try:
            return self.request.user.user_profile
        except UserProfile.DoesNotExist:
            raise NotFound("UserProfile matching query does not exist.")
        
    def get_user_profile_by_id(self, user_id):
        if not self.request.user.is_authenticated:
            raise NotAuthenticated("User is not authenticated.")
        user_id= self.kwargs.get('user_id') or self.request.data.get('user') or self.request.query_params.get('user')
        if not user_id:
            raise NotFound("User ID not provided.")
        try:
            return UserProfile.objects.get(user__id=user_id)
        except UserProfile.DoesNotExist:
            raise NotFound("User profile matching query does not exist.")
    
    def get_post(self):
        post_id = self.kwargs.get('post_id') or self.request.data.get('post') or self.request.query_params.get('post')
        if not post_id:
            raise NotFound("Post ID not provided.")
        try:
            return Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise NotFound("Post matching query does not exist.")