from rest_framework.exceptions import NotFound
from accounts.models import UserProfile
from .models import Event
from rest_framework.exceptions import NotAuthenticated

class GetUserProfileAndEventMixin:
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
    
    def get_event(self):
        event_id = self.kwargs.get('event_id') or self.request.data.get('event') or self.request.query_params.get('event')
        if not event_id:
            raise NotFound("Event ID not provided.")
        try:
            return Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            raise NotFound("Event matching query does not exist.")