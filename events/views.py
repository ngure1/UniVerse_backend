from .models import Event
from accounts.models import UserProfile
from rest_framework import generics,status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import EventSerializer
from posts.mixins import GetUserProfileAndPostMixin
from posts.permissions import IsOwnerOrReadOnly
from rest_framework.exceptions import NotFound
from accounts.pagination import CustomPagination
from rest_framework.response import Response
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

    # list all events* // create a new event
class ListCreateEvent(generics.ListCreateAPIView, GetUserProfileAndPostMixin):
    queryset = Event.objects.all().order_by('-created_at')
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination
    
    def perform_create(self, serializer):
        user_profile = self.get_user_profile()
        serializer.save(author=user_profile)

    # retrieve a single instance of event, update and delete
class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all().order_by('-created_at')
    serializer_class = EventSerializer
    permission_classes = [IsOwnerOrReadOnly]


    # get all events by a specific user
class UserEventsList(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        try:
            user_profile = UserProfile.objects.get(user__id=user_id)
            events=Event.objects.filter(author=user_profile)
            if not events.exists():
                raise NotFound("This user does not have any event postings.")
        except UserProfile.DoesNotExist:
            raise NotFound("User profile does not exist")
        


class EventSearchView(generics.GenericAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q', '')

        if not query:
            return Response({'error': _('Query parameter "q" is required.')}, status=status.HTTP_400_BAD_REQUEST)

        event_results = Event.objects.filter(
            Q(title__icontains=query) |
            Q(author__user__email__icontains=query) |
            Q(author__user__first_name__icontains=query) |
            Q(description__icontains=query)
        ).order_by('-created_at')

        event_serializer = self.get_serializer(event_results, many=True)
        return Response({'Events': event_serializer.data})






